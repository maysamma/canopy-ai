from pathlib import Path
from uuid import uuid4

from fastapi import (
    APIRouter,
    Depends,
    File,
    HTTPException,
    UploadFile,
)
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.models.project import Project
from app.services.analysis_service import analyze_urban_image
from app.services.image_generation_service import generate_improved_image
from app.services.report_service import generate_pdf_report



router = APIRouter(
    prefix="/api/projects",
    tags=["Projects"],
)

UPLOAD_DIR = Path(__file__).resolve().parents[2] / "uploads"
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

ALLOWED_TYPES = {
    "image/jpeg",
    "image/png",
    "image/webp",
}

MAX_FILE_SIZE = 10 * 1024 * 1024


def project_to_dict(project: Project) -> dict:
    return {
        "id": project.id,
        "filename": project.filename,
        "image_url": project.image_url,
        "status": project.status,
        "analysis": project.analysis,
        "generated_image_url": project.generated_image_url,
        "visualization_status": project.visualization_status,
        "created_at": project.created_at.isoformat(),
    }


@router.post("", status_code=201)
async def create_project(
    image: UploadFile = File(...),
    db: Session = Depends(get_db),
) -> dict:
    """
    Upload an urban image, analyze it, and save the project
    permanently in SQLite.
    """

    if image.content_type not in ALLOWED_TYPES:
        raise HTTPException(
            status_code=415,
            detail="Upload JPG, PNG, or WEBP images only.",
        )

    content = await image.read()

    if not content:
        raise HTTPException(
            status_code=400,
            detail="The uploaded file is empty.",
        )

    if len(content) > MAX_FILE_SIZE:
        raise HTTPException(
            status_code=413,
            detail="Maximum file size is 10 MB.",
        )

    project_id = uuid4().hex[:8]
    original_filename = image.filename or "street.jpg"

    suffix = Path(original_filename).suffix.lower()

    if suffix not in {".jpg", ".jpeg", ".png", ".webp"}:
        suffix = ".jpg"

    saved_name = f"{project_id}{suffix}"
    saved_path = UPLOAD_DIR / saved_name
    image_url = f"/uploads/{saved_name}"

    try:
        saved_path.write_bytes(content)

    except OSError as exc:
        raise HTTPException(
            status_code=500,
            detail="The image could not be saved.",
        ) from exc

    try:
        analysis = analyze_urban_image(saved_path)

    except ValueError as exc:
        saved_path.unlink(missing_ok=True)

        raise HTTPException(
            status_code=400,
            detail=str(exc),
        ) from exc

    except RuntimeError as exc:
        saved_path.unlink(missing_ok=True)

        print(f"Vision analysis failed: {exc}")

        raise HTTPException(
            status_code=502,
            detail=(
                "Vision analysis is temporarily unavailable. "
                "Please try again."
            ),
        ) from exc

    except Exception as exc:
        saved_path.unlink(missing_ok=True)

        print("\n========== PROJECT ANALYSIS ERROR ==========")
        print(f"Error type: {type(exc).__name__}")
        print(f"Error message: {exc}")
        print("============================================\n")

        raise HTTPException(
            status_code=500,
            detail="An unexpected analysis error occurred.",
        ) from exc

    project = Project(
        id=project_id,
        filename=original_filename,
        image_url=image_url,
        status="completed",
        analysis=analysis,
    )

    try:
        db.add(project)
        db.commit()
        db.refresh(project)

    except Exception as exc:
        db.rollback()
        saved_path.unlink(missing_ok=True)

        print("\n========== DATABASE SAVE ERROR ==========")
        print(f"Error type: {type(exc).__name__}")
        print(f"Error message: {exc}")
        print("=========================================\n")

        raise HTTPException(
            status_code=500,
            detail="The project could not be saved.",
        ) from exc

    return project_to_dict(project)


@router.get("")
def list_projects(
    db: Session = Depends(get_db),
) -> list[dict]:
    """
    Return all projects stored in SQLite,
    ordered from newest to oldest.
    """

    projects = (
        db.query(Project)
        .order_by(Project.created_at.desc())
        .all()
    )

    return [
        project_to_dict(project)
        for project in projects
    ]


@router.get("/{project_id}")
def get_project(
    project_id: str,
    db: Session = Depends(get_db),
) -> dict:
    """
    Return a project stored in SQLite.
    """

    project = db.get(Project, project_id)

    if project is None:
        raise HTTPException(
            status_code=404,
            detail="Project not found.",
        )

    return project_to_dict(project)

@router.get("/{project_id}/report")
def download_project_report(
    project_id: str,
    db: Session = Depends(get_db),
):
    """
    Generate and download a PDF report for a stored project.
    """

    project = db.get(Project, project_id)

    if project is None:
        raise HTTPException(
            status_code=404,
            detail="Project not found.",
        )

    report_path = generate_pdf_report(
        project_to_dict(project)
    )

    return FileResponse(
        path=report_path,
        media_type="application/pdf",
        filename=f"canopy-report-{project_id}.pdf",
    )


@router.post("/{project_id}/visualization")
def generate_project_visualization(
    project_id: str,
    db: Session = Depends(get_db),
) -> dict:
    """
    Generate an improved visualization for an existing project.
    """

    project = db.get(Project, project_id)

    if project is None:
        raise HTTPException(
            status_code=404,
            detail="Project not found.",
        )

    if not project.image_url:
        raise HTTPException(
            status_code=400,
            detail="The project does not contain an uploaded image.",
        )

    analysis = project.analysis or {}
    visualization_prompt = analysis.get("visualization_prompt")

    if not visualization_prompt:
        raise HTTPException(
            status_code=400,
            detail="The visualization prompt is missing.",
        )

    source_filename = Path(project.image_url).name
    source_image_path = UPLOAD_DIR / source_filename

    try:
        generated_path = generate_improved_image(
            source_image_path=source_image_path,
            prompt=visualization_prompt,
            project_id=project_id,
        )

    except FileNotFoundError as exc:
        raise HTTPException(
            status_code=404,
            detail=str(exc),
        ) from exc

    except RuntimeError as exc:
        print(f"Image generation failed: {exc}")

        project.visualization_status = "unavailable"
        db.commit()

        raise HTTPException(
            status_code=503,
            detail=str(exc),
        ) from exc

    except Exception as exc:
        print("\n========== IMAGE GENERATION ERROR ==========")
        print(f"Error type: {type(exc).__name__}")
        print(f"Error message: {exc}")
        print("============================================\n")

        project.visualization_status = "failed"
        db.commit()

        raise HTTPException(
            status_code=500,
            detail="An unexpected image-generation error occurred.",
        ) from exc

    generated_image_url = f"/generated/{generated_path.name}"

    project.generated_image_url = generated_image_url
    project.visualization_status = "completed"

    db.commit()
    db.refresh(project)

    return {
        "project_id": project.id,
        "status": "completed",
        "generated_image_url": project.generated_image_url,
    }
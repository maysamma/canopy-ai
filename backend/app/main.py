from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from app.routes.projects import router as projects_router

from app.database.base import Base
from app.database.session import engine
from app.models.project import Project

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Canopy AI API",
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

backend_dir = Path(__file__).resolve().parents[1]

uploads_dir = backend_dir / "uploads"
uploads_dir.mkdir(parents=True, exist_ok=True)

generated_dir = backend_dir / "generated"
generated_dir.mkdir(parents=True, exist_ok=True)

app.mount(
    "/uploads",
    StaticFiles(directory=uploads_dir),
    name="uploads",
)

app.mount(
    "/generated",
    StaticFiles(directory=generated_dir),
    name="generated",
)

app.include_router(projects_router)


@app.get("/api/health")
def health() -> dict:
    return {
        "status": "ok",
        "service": "Canopy AI API",
    }
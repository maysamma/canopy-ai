from pathlib import Path
from datetime import datetime

from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.lib import colors

from reportlab.platypus import (
    Image,
    KeepTogether,
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)

BASE_DIR = Path(__file__).resolve().parents[2]

REPORTS_DIR = BASE_DIR / "reports"
UPLOADS_DIR = BASE_DIR / "uploads"
GENERATED_DIR = BASE_DIR / "generated"

REPORTS_DIR.mkdir(parents=True, exist_ok=True)


def generate_pdf_report(project: dict) -> Path:
    """
    Generate a PDF report for a Canopy AI project.
    """

    output_path = REPORTS_DIR / f"{project['id']}.pdf"

    styles = getSampleStyleSheet()
    created_at = datetime.fromisoformat(
        project["created_at"]
    ).strftime("%d %b %Y, %H:%M")

    document = SimpleDocTemplate(
        str(output_path),
        pagesize=A4,
    )

    story = [
        Paragraph("Canopy AI Report", styles["Title"]),
        Paragraph(
            "AI-powered Urban Improvement Assistant",
            styles["Heading2"],
        ),
        Spacer(1, 18),
        
        Table(
            [
                ["Project ID", project["id"]],
                ["Original File", project["filename"]],
                ["Status", project["status"].title()],
                ["Created At", created_at],
            ],
            colWidths=[110, 260],
            style=TableStyle(
                [
                    (
                        "BACKGROUND",
                        (0, 0),
                        (0, -1),
                        colors.HexColor("#E1F1E7"),
                    ),
                    (
                        "TEXTCOLOR",
                        (0, 0),
                        (0, -1),
                        colors.HexColor("#176641"),
                    ),
                    (
                        "FONTNAME",
                        (0, 0),
                        (0, -1),
                        "Helvetica-Bold",
                    ),
                    (
                        "GRID",
                        (0, 0),
                        (-1, -1),
                        0.5,
                        colors.HexColor("#A9C7B5"),
                    ),
                    (
                        "TOPPADDING",
                        (0, 0),
                        (-1, -1),
                        8,
                    ),
                    (
                        "BOTTOMPADDING",
                        (0, 0),
                        (-1, -1),
                        8,
                    ),
                ]
            ),
        ),
        Spacer(1, 18),

    ]

    image_url = project.get("image_url")

    if image_url:
        image_filename = Path(image_url).name
        image_path = UPLOADS_DIR / image_filename

        if image_path.exists():
            story.extend(
                [
                    Paragraph(
                        "Original Urban Image",
                        styles["Heading2"],
                    ),
                    Spacer(1, 8),
                    Image(
                        str(image_path),
                        width=5.5 * inch,
                        height=4 * inch,
                        kind="proportional",
                    ),
                    Spacer(1, 16),
                ]
            )

    generated_image_url = project.get("generated_image_url")

    if generated_image_url:
        generated_filename = Path(generated_image_url).name
        generated_image_path = GENERATED_DIR / generated_filename

        if generated_image_path.exists():
            story.extend(
                [
                    Paragraph(
                        "Improved Urban Visualization",
                        styles["Heading2"],
                    ),
                    Spacer(1, 8),
                    Image(
                        str(generated_image_path),
                        width=5.5 * inch,
                        height=4 * inch,
                        kind="proportional",
                    ),
                    Spacer(1, 16),
                ]
            )

    story.extend(
        [
            Paragraph("Summary", styles["Heading2"]),
            Paragraph(
                project["analysis"]["summary"],
                styles["BodyText"],
            ),
            Spacer(1, 12),

            KeepTogether(
                [
                    Paragraph(
                        "Assessment Scores",
                        styles["Heading2"],
                    ),
                    Table(
                        [
                            ["Metric", "Value"],
                            [
                                "Green Coverage",
                                f"{project['analysis']['scores']['green_coverage']}%",
                            ],
                            [
                                "Walkability",
                                f"{project['analysis']['scores']['walkability']}%",
                            ],
                            [
                                "Shade",
                                f"{project['analysis']['scores']['shade']}%",
                            ],
                            [
                                "Solar Potential",
                                f"{project['analysis']['scores']['solar_potential']}%",
                            ],
                            [
                                "Heat Risk",
                                str(project["analysis"]["scores"]["heat_risk"]),
                            ],
                        ],
                        colWidths=[220, 120],
                        repeatRows=1,
                        style=TableStyle(
                            [
                                (
                                    "BACKGROUND",
                                    (0, 0),
                                    (-1, 0),
                                    colors.HexColor("#176641"),
                                ),
                                (
                                    "TEXTCOLOR",
                                    (0, 0),
                                    (-1, 0),
                                    colors.white,
                                ),
                                (
                                    "GRID",
                                    (0, 0),
                                    (-1, -1),
                                    0.5,
                                    colors.grey,
                                ),
                                (
                                    "BACKGROUND",
                                    (0, 1),
                                    (-1, -1),
                                    colors.whitesmoke,
                                ),
                                (
                                    "BOTTOMPADDING",
                                    (0, 0),
                                    (-1, 0),
                                    10,
                                ),
                                (
                                    "TOPPADDING",
                                    (0, 1),
                                    (-1, -1),
                                    8,
                                ),
                                (
                                    "BOTTOMPADDING",
                                    (0, 1),
                                    (-1, -1),
                                    8,
                                ),
                                (
                                    "FONTNAME",
                                    (0, 0),
                                    (-1, 0),
                                    "Helvetica-Bold",
                                ),
                                (
                                    "ALIGN",
                                    (1, 0),
                                    (1, -1),
                                    "CENTER",
                                ),
                            ]
                        ),
                    ),
                ]
            ),

            Spacer(1, 16),

            Paragraph("Current Issues", styles["Heading2"]),
        ]
    )

    for issue in project["analysis"]["issues"]:
        story.append(
            Paragraph(
                f"- {issue}",
                styles["BodyText"],
            )
        )

    story.extend(
        [
            Spacer(1, 12),
            Paragraph(
                "Recommendations & Expected Impact",
                styles["Heading2"],
            ),
        ]
    )

    for item in project["analysis"]["recommendations"]:
        story.extend(
            [
                Paragraph(
                    f"<b>{item['title']}</b><br/>"
                    f"Action: {item['action']}<br/>"
                    f"Expected Impact: {item['impact']}<br/>"
                    f"Priority: {item['priority']}",
                    styles["BodyText"],
                ),
                Spacer(1, 10),
            ]
        )

    document.build(story)

    return output_path
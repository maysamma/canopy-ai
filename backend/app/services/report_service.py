from pathlib import Path
from datetime import datetime

from reportlab.platypus import Image

from reportlab.lib.pagesizes import A4

from reportlab.lib.styles import (
    ParagraphStyle,
    getSampleStyleSheet,
)

from app.services.analysis_service import calculate_overall_score

from reportlab.lib.units import inch
from reportlab.lib import colors

from reportlab.platypus import (
    Image,
    KeepTogether,
    PageBreak,
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

def normalize_score(value) -> int:
    """
    Convert a score into an integer from 0 to 100.

    This also supports older projects where heat risk
    may have been stored as High, Medium, or Low.
    """

    if isinstance(value, str):
        text_value = value.strip().lower()

        legacy_heat_risk = {
            "low": 20,
            "medium": 50,
            "high": 80,
        }

        if text_value in legacy_heat_risk:
            return legacy_heat_risk[text_value]

    try:
        numeric_value = float(value)
    except (TypeError, ValueError):
        return 0

    return round(
        max(0, min(100, numeric_value))
    )


def calculate_overall_score(scores: dict) -> int:
    green_coverage = normalize_score(
        scores.get("green_coverage")
    )
    walkability = normalize_score(
        scores.get("walkability")
    )
    shade = normalize_score(
        scores.get("shade")
    )
    solar_potential = normalize_score(
        scores.get("solar_potential")
    )
    heat_risk = normalize_score(
        scores.get("heat_risk")
    )

    heat_comfort = 100 - heat_risk

    return round(
        (
            green_coverage
            + walkability
            + shade
            + solar_potential
            + heat_comfort
        )
        / 5
    )


def get_score_status(score: int) -> str:
    if score >= 75:
        return "Strong"

    if score >= 50:
        return "Moderate"

    return "Needs Improvement"


def get_heat_risk_status(score: int) -> str:
    if score <= 25:
        return "Low Risk"

    if score <= 50:
        return "Moderate Risk"

    return "High Risk"


def get_status_color(status: str) -> str:
    status_colors = {
        "Strong": "#2E7D32",
        "Moderate": "#C47F00",
        "Needs Improvement": "#C62828",
        "Low Risk": "#2E7D32",
        "Moderate Risk": "#C47F00",
        "High Risk": "#C62828",
    }

    return status_colors.get(status, "#557064")


def draw_page_header_footer(
    canvas,
    document,
) -> None:
    """
    Draw a consistent header and footer on every report page.
    """

    canvas.saveState()

    page_width, page_height = A4

    canvas.setStrokeColor(
        colors.HexColor("#D5E7DC")
    )
    canvas.setLineWidth(0.8)

    canvas.line(
        document.leftMargin,
        page_height - 42,
        page_width - document.rightMargin,
        page_height - 42,
    )

    canvas.setFillColor(
        colors.HexColor("#176641")
    )
    canvas.setFont(
        "Helvetica-Bold",
        10,
    )

    canvas.drawString(
        document.leftMargin,
        page_height - 32,
        "Canopy AI",
    )

    canvas.setFillColor(
        colors.HexColor("#557064")
    )
    canvas.setFont(
        "Helvetica",
        8,
    )

    canvas.drawRightString(
        page_width - document.rightMargin,
        page_height - 32,
        "Urban Improvement Assessment",
    )

    canvas.line(
        document.leftMargin,
        42,
        page_width - document.rightMargin,
        42,
    )

    canvas.setFont(
        "Helvetica",
        7.5,
    )

    canvas.drawString(
        document.leftMargin,
        29,
        (
            "Preliminary AI-generated indicators — "
            "not a professional engineering or municipal assessment."
        ),
    )

    canvas.drawRightString(
        page_width - document.rightMargin,
        29,
        f"Page {canvas.getPageNumber()}",
    )

    canvas.restoreState()

    


def build_cover_page(
    story,
    styles,
    project,
    analysis,
    overall_score,
    created_at,
):
    """
    Build the report cover page.
    """

    if overall_score >= 85:
        overall_label = "Excellent"
        label_color = "#1B8F4D"

    elif overall_score >= 70:
        overall_label = "Strong"
        label_color = "#1B8F4D"

    elif overall_score >= 50:
        overall_label = "Moderate"
        label_color = "#C68A00"

    else:
        overall_label = "Needs Improvement"
        label_color = "#C0392B"

    logo_path = (
        BASE_DIR
        / "assets"
        / "canopy_logo1.png"
    )

    if logo_path.exists():
        story.append(
            Image(
                str(logo_path),
                width=5.5 * inch,
                height=2.3 * inch,
                kind="proportional",
                hAlign="CENTER",
            )
        )

    story.extend(
        [
            Spacer(1, 2),

            Paragraph(
                "Urban Improvement Assessment Report",
                styles["Title"],
            ),

            Spacer(1, 3),

            Paragraph(
                (
                    '<para align="center">'
                    "AI-powered Urban Improvement Assistant"
                    "</para>"
                ),
                styles["BodyText"],
            ),

        ]
    )


    story.append(Spacer(1, 2))

    score_title_style = ParagraphStyle(
        name="ScoreTitle",
        parent=styles["BodyText"],
        fontName="Helvetica-Bold",
        fontSize=10,
        leading=12,
        alignment=1,
        textColor=colors.HexColor("#176641"),
    )

    score_value_style = ParagraphStyle(
        name="ScoreValue",
        parent=styles["BodyText"],
        fontName="Helvetica-Bold",
        fontSize=40,
        leading=42,
        alignment=1,
        textColor=colors.HexColor("#176641"),
    )

    score_label_style = ParagraphStyle(
        name="ScoreLabel",
        parent=styles["BodyText"],
        fontName="Helvetica-Bold",
        fontSize=12,
        leading=16,
        alignment=1,
        textColor=colors.HexColor(label_color),
    )

    score_card = Table(
        [
            [
                Paragraph(
                    "OVERALL URBAN SCORE",
                    score_title_style,
                )
            ],
            [
                Table(
                    [
                        [
                            Paragraph(
                                str(overall_score),
                                score_value_style,
                            ),
                            Paragraph(
                                "/ 100",
                                ParagraphStyle(
                                    name="ScoreSuffix",
                                    parent=styles["BodyText"],
                                    fontSize=12,
                                    leading=14,
                                    alignment=0,
                                    textColor=colors.HexColor(
                                        "#557064"
                                    ),
                                ),
                            ),
                        ]
                    ],
                    colWidths=[90, 55],
                    hAlign="CENTER",
                    style=TableStyle(
                        [
                            (
                                "VALIGN",
                                (0, 0),
                                (-1, -1),
                                "BOTTOM",
                            ),
                            (
                                "LEFTPADDING",
                                (0, 0),
                                (-1, -1),
                                0,
                            ),
                            (
                                "RIGHTPADDING",
                                (0, 0),
                                (-1, -1),
                                0,
                            ),
                            (
                                "TOPPADDING",
                                (0, 0),
                                (-1, -1),
                                0,
                            ),
                            (
                                "BOTTOMPADDING",
                                (0, 0),
                                (-1, -1),
                                0,
                            ),
                        ]
                    ),
                )
            ],
            [
                Paragraph(
                    overall_label,
                    score_label_style,
                )
            ],
        ],
        colWidths=[360],
        rowHeights=[30, 68, 42],
        hAlign="CENTER",
        style=TableStyle(
            [
                (
                    "BACKGROUND",
                    (0, 0),
                    (-1, -1),
                    colors.HexColor("#F3F8F5"),
                ),
                (
                    "BOX",
                    (0, 0),
                    (-1, -1),
                    1,
                    colors.HexColor("#176641"),
                ),
                (
                    "ALIGN",
                    (0, 0),
                    (-1, -1),
                    "CENTER",
                ),
                (
                    "VALIGN",
                    (0, 0),
                    (-1, -1),
                    "MIDDLE",
                ),
                (
                    "LEFTPADDING",
                    (0, 0),
                    (-1, -1),
                    12,
                ),
                (
                    "RIGHTPADDING",
                    (0, 0),
                    (-1, -1),
                    12,
                ),
                (
                    "TOPPADDING",
                    (0, 0),
                    (-1, -1),
                    0,
                ),
                (
                    "BOTTOMPADDING",
                    (0, 0),
                    (-1, -1),
                    0,
                ),
            ]
        ),
    )

    story.append(Spacer(1, 6))
    story.append(score_card)
    story.append(Spacer(1, 18))


    story.extend(
        [

            Paragraph(
                "Project Information",
                styles["SectionTitle"],
            ),
            Spacer(1, 6),

            Table(
                [
                    ["Project ID", project["id"]],
                    [
                        "Status",
                        project["status"].title(),
                    ],
                    [
                        "Scene Type",
                        analysis["scene"]["scene_type"],
                    ],
                    ["Created At", created_at],
                ],
                colWidths=[140, 280],
                style=TableStyle(
                    [
                        (
                            "BACKGROUND",
                            (0, 0),
                            (0, -1),
                            colors.HexColor("#F8FCFA"),
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
                            colors.HexColor("#BFD8CB"),
                        ),
                        (
                            "TOPPADDING",
                            (0, 0),
                            (-1, -1),
                            12,
                        ),
                        (
                            "BOTTOMPADDING",
                            (0, 0),
                            (-1, -1),
                            12,
                        ),
                    ]
                ),
            ),

            Spacer(1, 24),

            Paragraph(
                (
                    '<para align="center">'
                    "<b>Prepared by Canopy AI</b>"
                    "</para>"
                ),
                styles["BodyText"],
            ),

            Spacer(1, 4),

            Paragraph(
                (
                    '<para align="center">'
                    "AI-powered Urban Planning Platform"
                    "</para>"
                ),
                styles["BodyText"],
            ),

            Spacer(1, 4),

            Paragraph(
                (
                    '<para align="center">'
                    "Version 1.0"
                    "</para>"
                ),
                styles["BodyText"],
            ),
        ]
    )
    
            



def generate_pdf_report(project: dict) -> Path:
    """
    Generate a PDF report for a Canopy AI project.
    """

    output_path = REPORTS_DIR / f"{project['id']}.pdf"

    styles = getSampleStyleSheet()
    styles.add(
        ParagraphStyle(
            name="SectionTitle",
            parent=styles["Heading2"],
            fontSize=12,
            leading=15,
            spaceBefore=6,
            spaceAfter=6,
            textColor=colors.HexColor("#176641"),
        )
    )
    styles["Title"].textColor = colors.HexColor("#176641")
    styles["Title"].fontName = "Helvetica-Bold"
    styles["Title"].fontSize = 26
    styles["Title"].leading = 32
    styles["Title"].spaceAfter = 6

    styles["Heading2"].textColor = colors.HexColor("#176641")
    styles["Heading2"].fontName = "Helvetica-Bold"
    styles["Heading2"].fontSize = 14
    styles["Heading2"].leading = 18
    styles["Heading2"].spaceBefore = 8
    styles["Heading2"].spaceAfter = 8

    styles["BodyText"].textColor = colors.HexColor("#33443C")
    styles["BodyText"].fontSize = 9.5
    styles["BodyText"].leading = 14


    created_at = datetime.fromisoformat(
        project["created_at"]
    ).strftime("%d %b %Y, %H:%M")

    analysis = project["analysis"]
    scores = analysis["scores"]
    overall_score = calculate_overall_score(scores)

    green = normalize_score(scores["green_coverage"])
    walkability = normalize_score(scores["walkability"])
    shade = normalize_score(scores["shade"])
    solar = normalize_score(scores["solar_potential"])
    heat = normalize_score(scores["heat_risk"])

    document = SimpleDocTemplate(
    str(output_path),
    pagesize=A4,
    rightMargin=42,
    leftMargin=42,
    topMargin=58,
    bottomMargin=58,
)

    story = []

    build_cover_page(
        story=story,
        styles=styles,
        project=project,
        analysis=analysis,
        overall_score=overall_score,
        created_at=created_at,
    )

    story.extend(
        [
            PageBreak(),

            Paragraph(
                "Executive Summary",
                styles["Heading2"],
            ),

            Table(
                [
                    [
                        Table(
                            [
                                [
                                    Paragraph(
                                        (
                                            "<font color='#176641' size='11'>"
                                            "<b>AI URBAN ASSESSMENT</b>"
                                            "</font>"
                                        ),
                                        styles["BodyText"],
                                    )
                                ],
                                [
                                    Paragraph(
                                        analysis["summary"],
                                        styles["BodyText"],
                                    )
                                ],
                            ],
                            colWidths=[412],
                            style=TableStyle(
                                [
                                    (
                                        "BACKGROUND",
                                        (0, 0),
                                        (-1, -1),
                                        colors.HexColor("#F3F8F5"),
                                    ),
                                    (
                                        "LINEBELOW",
                                        (0, 0),
                                        (-1, 0),
                                        0.5,
                                        colors.HexColor("#D5E6DC"),
                                    ),
                                    (
                                        "LEFTPADDING",
                                        (0, 0),
                                        (-1, -1),
                                        0,
                                    ),
                                    (
                                        "RIGHTPADDING",
                                        (0, 0),
                                        (-1, -1),
                                        0,
                                    ),
                                    (
                                        "TOPPADDING",
                                        (0, 0),
                                        (-1, 0),
                                        0,
                                    ),
                                    (
                                        "BOTTOMPADDING",
                                        (0, 0),
                                        (-1, 0),
                                        8,
                                    ),
                                    (
                                        "TOPPADDING",
                                        (0, 1),
                                        (-1, 1),
                                        10,
                                    ),
                                    (
                                        "BOTTOMPADDING",
                                        (0, 1),
                                        (-1, 1),
                                        0,
                                    ),
                                ]
                            ),
                        )
                    ]
                ],
                colWidths=[440],
                style=TableStyle(
                    [
                        (
                            "BACKGROUND",
                            (0, 0),
                            (-1, -1),
                            colors.HexColor("#F3F8F5"),
                        ),
                        (
                            "BOX",
                            (0, 0),
                            (-1, -1),
                            0.7,
                            colors.HexColor("#B7D4C4"),
                        ),
                        (
                            "LINEBEFORE",
                            (0, 0),
                            (0, -1),
                            4,
                            colors.HexColor("#176641"),
                        ),
                        (
                            "LEFTPADDING",
                            (0, 0),
                            (-1, -1),
                            18,
                        ),
                        (
                            "RIGHTPADDING",
                            (0, 0),
                            (-1, -1),
                            16,
                        ),
                        (
                            "TOPPADDING",
                            (0, 0),
                            (-1, -1),
                            14,
                        ),
                        (
                            "BOTTOMPADDING",
                            (0, 0),
                            (-1, -1),
                            14,
                        ),
                    ]
                ),
            ),

            Spacer(1, 18),
        ]

    )

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
                    Spacer(1, 6),
                    Table(
                        [
                            [
                                Image(
                                    str(image_path),
                                    width=5.2 * inch,
                                    height=3.7 * inch,
                                    kind="proportional",
                                )
                            ],
                            [
                                Paragraph(
                                    (
                                        "<font color='#557064' size='9'>"
                                        "Uploaded scene used as the visual input "
                                        "for the urban assessment."
                                        "</font>"
                                    ),
                                    styles["BodyText"],
                                )
                            ],
                        ],
                        colWidths=[5.45 * inch],
                        style=TableStyle(
                            [
                                (
                                    "BACKGROUND",
                                    (0, 0),
                                    (-1, -1),
                                    colors.white,
                                ),
                                (
                                    "BOX",
                                    (0, 0),
                                    (-1, -1),
                                    0.7,
                                    colors.HexColor("#C8DDD1"),
                                ),
                                (
                                    "LINEABOVE",
                                    (0, 1),
                                    (-1, 1),
                                    0.5,
                                    colors.HexColor("#DCE9E1"),
                                ),
                                (
                                    "ALIGN",
                                    (0, 0),
                                    (-1, 0),
                                    "CENTER",
                                ),
                                (
                                    "LEFTPADDING",
                                    (0, 0),
                                    (-1, 0),
                                    8,
                                ),
                                (
                                    "RIGHTPADDING",
                                    (0, 0),
                                    (-1, 0),
                                    8,
                                ),
                                (
                                    "TOPPADDING",
                                    (0, 0),
                                    (-1, 0),
                                    8,
                                ),
                                (
                                    "BOTTOMPADDING",
                                    (0, 0),
                                    (-1, 0),
                                    8,
                                ),
                                (
                                    "LEFTPADDING",
                                    (0, 1),
                                    (-1, 1),
                                    12,
                                ),
                                (
                                    "RIGHTPADDING",
                                    (0, 1),
                                    (-1, 1),
                                    12,
                                ),
                                (
                                    "TOPPADDING",
                                    (0, 1),
                                    (-1, 1),
                                    7,
                                ),
                                (
                                    "BOTTOMPADDING",
                                    (0, 1),
                                    (-1, 1),
                                    7,
                                ),
                            ]
                        ),
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
            
            KeepTogether(
                [
                    Paragraph(
                        "Assessment Scores",
                        styles["Heading2"],
                    ),
                    Table(
                        [
                            ["Metric", "Score", "Status"],

                            [
                                "Green Coverage",
                                f"{green}%",
                                Paragraph(
                                    (
                                        f"<font color='{get_status_color(get_score_status(green))}'>"
                                        f"<b>{get_score_status(green)}</b>"
                                        "</font>"
                                    ),
                                    styles["BodyText"],
                                ),
                            ],

                            [
                                "Walkability",
                                f"{walkability}%",
                                Paragraph(
                                    (
                                        f"<font color='{get_status_color(get_score_status(walkability))}'>"
                                        f"<b>{get_score_status(walkability)}</b>"
                                        "</font>"
                                    ),
                                    styles["BodyText"],
                                ),
                            ],

                            [
                                "Shade",
                                f"{shade}%",
                                Paragraph(
                                    (
                                        f"<font color='{get_status_color(get_score_status(shade))}'>"
                                        f"<b>{get_score_status(shade)}</b>"
                                        "</font>"
                                    ),
                                    styles["BodyText"],
                                ),
                            ],

                            [
                                "Solar Potential",
                                f"{solar}%",
                                Paragraph(
                                    (
                                        f"<font color='{get_status_color(get_score_status(solar))}'>"
                                        f"<b>{get_score_status(solar)}</b>"
                                        "</font>"
                                    ),
                                    styles["BodyText"],
                                ),
                            ],

                            [
                                "Heat Risk",
                                str(heat),
                                Paragraph(
                                    (
                                        f"<font color='{get_status_color(get_heat_risk_status(heat))}'>"
                                        f"<b>{get_heat_risk_status(heat)}</b>"
                                        "</font>"
                                    ),
                                    styles["BodyText"],
                                ),
                            ],
                        ],
                        colWidths=[190, 70, 130],
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
                                    "FONTNAME",
                                    (0, 0),
                                    (-1, 0),
                                    "Helvetica-Bold",
                                ),
                                (
                                    "GRID",
                                    (0, 0),
                                    (-1, -1),
                                    0.5,
                                    colors.HexColor("#D0D7D3"),
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
                                    "ALIGN",
                                    (1, 1),
                                    (2, -1),
                                    "CENTER",
                                ),
                            ]
                        ),
                    )
                ]
            ),

            Spacer(1, 16),

            Paragraph("Current Issues", styles["Heading2"]),
        ]
    )

    for issue_number, issue in enumerate(
        project["analysis"]["issues"],
        start=1,
    ):
        issue_card = Table(
            [
                [
                    Paragraph(
                        (
                            f"<font color='#C62828'>"
                            f"<b>{issue_number:02d}</b>"
                            "</font>"
                        ),
                        styles["BodyText"],
                    ),
                    Paragraph(
                        issue,
                        styles["BodyText"],
                    ),
                ]
            ],
            colWidths=[34, 406],
            style=TableStyle(
                [
                    (
                        "BACKGROUND",
                        (0, 0),
                        (-1, -1),
                        colors.HexColor("#FFF8F7"),
                    ),
                    (
                        "BOX",
                        (0, 0),
                        (-1, -1),
                        0.6,
                        colors.HexColor("#E8C5C1"),
                    ),
                    (
                        "LINEBEFORE",
                        (0, 0),
                        (0, -1),
                        4,
                        colors.HexColor("#C62828"),
                    ),
                    (
                        "VALIGN",
                        (0, 0),
                        (-1, -1),
                        "MIDDLE",
                    ),
                    (
                        "ALIGN",
                        (0, 0),
                        (0, -1),
                        "CENTER",
                    ),
                    (
                        "LEFTPADDING",
                        (0, 0),
                        (0, -1),
                        8,
                    ),
                    (
                        "RIGHTPADDING",
                        (0, 0),
                        (0, -1),
                        8,
                    ),
                    (
                        "LEFTPADDING",
                        (1, 0),
                        (1, -1),
                        12,
                    ),
                    (
                        "RIGHTPADDING",
                        (1, 0),
                        (1, -1),
                        12,
                    ),
                    (
                        "TOPPADDING",
                        (0, 0),
                        (-1, -1),
                        9,
                    ),
                    (
                        "BOTTOMPADDING",
                        (0, 0),
                        (-1, -1),
                        9,
                    ),
                ]
            ),
        )

        story.append(KeepTogether([issue_card, Spacer(1, 7)]))

    story.extend(
        [
            Spacer(1, 12),
            Paragraph(
                "Recommendations & Expected Impact",
                styles["Heading2"],
            ),
        ]
    )

    for item in analysis["recommendations"]:

        priority = item["priority"]

        if priority == "High":
            priority_color = "#D32F2F"
        elif priority == "Medium":
            priority_color = "#F9A825"
        else:
            priority_color = "#2E7D32"

        left_border_color = colors.HexColor(priority_color)

        recommendation_card = Table(
            [[
                Paragraph(
                    f"""
                    <font color="#176641"><b>{item['title']}</b></font>
                    <br/><br/>

                    <b>Priority:</b>
                    <font color="{priority_color}">
                    <b>{priority}</b>
                    </font>

                    <br/><br/>

                    <b>Recommended Action</b>

                    <br/>

                    {item['action']}

                    <br/><br/>

                    <b>Expected Impact</b>

                    <br/>

                    {item['impact']}
                    """,
                    styles["BodyText"],
                )
            ]],
            colWidths=[440],
            style=TableStyle(
                [
                    (
                        "BACKGROUND",
                        (0, 0),
                        (-1, -1),
                        colors.HexColor("#F8FBF9"),
                    ),
                    (
                        "BOX",
                        (0, 0),
                        (-1, -1),
                        0.7,
                        colors.HexColor("#C6DDD0"),
                    ),
                    (
                        "LEFTPADDING",
                        (0, 0),
                        (-1, -1),
                        14,
                    ),
                    (
                        "RIGHTPADDING",
                        (0, 0),
                        (-1, -1),
                        14,
                    ),
                    (
                        "TOPPADDING",
                        (0, 0),
                        (-1, -1),
                        12,
                    ),
                    (
                        "BOTTOMPADDING",
                        (0, 0),
                        (-1, -1),
                        12,
                    ),
                    (
                        "LINEBEFORE",
                        (0, 0),
                        (0, -1),
                        4,
                        left_border_color,
                    ),
                ]
            ),
        )

        story.append(recommendation_card)
        story.append(Spacer(1, 12))

    story.extend(
            [
                Spacer(1, 2),
                Paragraph(
                    "Assessment Notes",
                    styles["Heading2"],
                ),
                Table(
                    [
                        [
                            Paragraph(
                                (
                                    "<font color='#176641'><b>Important:</b></font> "
                                    "These results are preliminary AI-generated "
                                    "indicators. Accuracy depends on image quality "
                                    "and scene suitability, and the report does not "
                                    "replace professional engineering, planning, "
                                    "environmental, or municipal review."
                                ),
                                styles["BodyText"],
                            )
                        ]
                    ],
                    colWidths=[440],
                    style=TableStyle(
                        [
                            (
                                "BACKGROUND",
                                (0, 0),
                                (-1, -1),
                                colors.HexColor("#F6F8F7"),
                            ),
                            (
                                "BOX",
                                (0, 0),
                                (-1, -1),
                                0.6,
                                colors.HexColor("#D5DEDA"),
                            ),
                            (
                                "LINEBEFORE",
                                (0, 0),
                                (0, -1),
                                4,
                                colors.HexColor("#176641"),
                            ),
                            (
                                "LEFTPADDING",
                                (0, 0),
                                (-1, -1),
                                14,
                            ),
                            (
                                "RIGHTPADDING",
                                (0, 0),
                                (-1, -1),
                                14,
                            ),
                            (
                                "TOPPADDING",
                                (0, 0),
                                (-1, -1),
                                9,
                            ),
                            (
                                "BOTTOMPADDING",
                                (0, 0),
                                (-1, -1),
                                9,
                            ),
                        ]
                    ),
                ),
            ]
        )

    document.build(
        story,
        onFirstPage=draw_page_header_footer,
        onLaterPages=draw_page_header_footer,
    )

    return output_path


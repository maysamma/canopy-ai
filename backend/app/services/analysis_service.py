from pathlib import Path

from PIL import Image, UnidentifiedImageError

from app.services.vision_service import analyze_image
from app.agents.visualization_agent import VisualizationAgent


def analyze_urban_image(image_path: Path) -> dict:
    """
    Analyze an uploaded urban image.

    The Vision Agent extracts the current scene information.
    This service then converts the Vision result into the response
    structure currently expected by the frontend.
    """

    if not image_path.exists():
        raise FileNotFoundError(f"Image was not found: {image_path}")

    try:
        with Image.open(image_path) as image:
            image.verify()

        with Image.open(image_path) as image:
            width, height = image.size

    except UnidentifiedImageError as error:
        raise ValueError("The uploaded file is not a valid image.") from error

    except OSError as error:
        raise ValueError("The uploaded image could not be opened.") from error

    vision_result = analyze_image(str(image_path))

    scores = calculate_scores(vision_result)

    issues = generate_initial_issues(
        vision_result=vision_result,
        scores=scores,
    )

    recommendations = generate_initial_recommendations(
        vision_result=vision_result,
        issues=issues,
    )

    visualization_agent = VisualizationAgent()

    visualization_prompt = visualization_agent.build_prompt(
        {
            "scene": {
                "image_width": width,
                "image_height": height,
                "scene_type": vision_result["scene_type"],
                "trees": vision_result["trees"],
                "sidewalk": vision_result["sidewalk"],
                "road": vision_result["road"],
                "buildings": vision_result["buildings"],
                "vehicles": vision_result["vehicles"],
                "empty_spaces": vision_result["empty_spaces"],
                "shade": vision_result["shade"],
            },
            "scores": scores,
            "issues": issues,
            "recommendations": recommendations,
        }
    )

    return {
        "scene": {
            "image_width": width,
            "image_height": height,
            "scene_type": vision_result["scene_type"],
            "trees": vision_result["trees"],
            "sidewalk": vision_result["sidewalk"],
            "road": vision_result["road"],
            "buildings": vision_result["buildings"],
            "vehicles": vision_result["vehicles"],
            "empty_spaces": vision_result["empty_spaces"],
            "shade": vision_result["shade"],
        },
        "scores": scores,
        "issues": issues,
        "recommendations": recommendations,
        "summary": generate_summary(
            vision_result=vision_result,
            scores=scores,
        ),
        "confidence": vision_result["confidence"],
        "visualization_prompt": visualization_prompt,
        "disclaimer": (
            "Canopy AI provides preliminary AI-generated urban indicators. "
            "The results are not engineering measurements, architectural approval, "
            "or municipal approval."
        ),
    }


def calculate_scores(vision_result: dict) -> dict:
    """
    Convert the Vision Agent observations into preliminary urban scores.

    These values are initial indicators only. Later, the Urban Planner Agent
    will replace this rule-based logic.
    """

    green_coverage = 50
    shade_score = 50
    walkability = 55
    solar_potential = 75

    trees = vision_result.get("trees", "unknown").lower()
    shade = vision_result.get("shade", "unknown").lower()
    sidewalk = vision_result.get("sidewalk", "unknown").lower()
    empty_spaces = vision_result.get("empty_spaces", "unknown").lower()

    if trees == "none":
        green_coverage = 10
    elif trees == "very few":
        green_coverage = 20
    elif trees == "few":
        green_coverage = 35
    elif trees == "some":
        green_coverage = 60
    elif trees == "many":
        green_coverage = 85
    else:
        green_coverage = 50

    if shade == "none":
        shade_score = 5
    elif shade == "very low":
        shade_score = 15
    elif shade == "low":
        shade_score = 30
    elif shade == "medium":
        shade_score = 60
    elif shade == "high":
        shade_score = 85
    else:
        shade_score = 50

    if sidewalk == "not available":
        walkability = 15
    elif sidewalk == "limited":
        walkability = 35
    elif sidewalk == "partially available":
        walkability = 50
    elif sidewalk == "available":
        walkability = 70
    elif sidewalk == "wide":
        walkability = 85
    else:
        walkability = 50

    if empty_spaces in {"available", "yes", "visible"}:
        solar_potential = 82

    heat_risk = determine_heat_risk(
        green_coverage=green_coverage,
        shade_score=shade_score,
    )

    return {
        "green_coverage": green_coverage,
        "walkability": walkability,
        "shade": shade_score,
        "solar_potential": solar_potential,
        "heat_risk": heat_risk,
    }


def determine_heat_risk(
    green_coverage: int,
    shade_score: int,
) -> str:
    average_score = (green_coverage + shade_score) / 2

    if average_score < 35:
        return "High"

    if average_score < 65:
        return "Medium"

    return "Low"


def generate_initial_issues(
    vision_result: dict,
    scores: dict,
) -> list[str]:
    issues: list[str] = []

    if scores["green_coverage"] < 40:
        issues.append("Low tree and vegetation coverage.")

    if scores["shade"] < 40:
        issues.append("Limited shade along pedestrian areas.")

    if scores["walkability"] < 55:
        issues.append("Pedestrian comfort and sidewalk continuity can be improved.")

    empty_spaces = vision_result.get("empty_spaces", "").lower()

    if empty_spaces in {"available", "yes", "visible"}:
        issues.append("Some open space may not be used effectively.")

    vehicles = vision_result.get("vehicles", "").lower()

    if vehicles in {"many", "high", "heavy"}:
        issues.append("Vehicle presence may reduce pedestrian comfort and safety.")

    if not issues:
        issues.append(
            "The scene has generally acceptable urban conditions, "
            "with opportunities for targeted improvements."
        )

    return issues


def generate_initial_recommendations(
    vision_result: dict,
    issues: list[str],
) -> list[dict]:
    recommendations: list[dict] = []

    trees = vision_result.get("trees", "").lower()
    shade = vision_result.get("shade", "").lower()
    sidewalk = vision_result.get("sidewalk", "").lower()
    empty_spaces = vision_result.get("empty_spaces", "").lower()

    if trees in {"none", "very few", "few"}:
        recommendations.append(
            {
                "title": "Add native shade trees",
                "action": (
                    "Plant drought-tolerant native trees along sidewalks "
                    "and suitable open edges."
                ),
                "impact": (
                    "More greenery, improved pedestrian comfort, "
                    "and lower perceived heat."
                ),
                "priority": "High",
            }
        )

    if shade in {"none", "very low", "low"}:
        recommendations.append(
            {
                "title": "Create shaded pedestrian routes",
                "action": (
                    "Add lightweight canopies, pergolas, or tree-based shade "
                    "along frequently used walking paths."
                ),
                "impact": "Improved walkability during hot periods.",
                "priority": "High",
            }
        )

    if sidewalk in {
        "not available",
        "none",
        "missing",
        "partially available",
        "narrow",
        "limited",
    }:
        recommendations.append(
            {
                "title": "Improve pedestrian paths",
                "action": (
                    "Provide a continuous, visible, and step-free pedestrian route "
                    "with safe crossing points."
                ),
                "impact": "Safer and more inclusive pedestrian movement.",
                "priority": "High",
            }
        )

    if empty_spaces in {"available", "yes", "visible"}:
        recommendations.append(
            {
                "title": "Activate unused open spaces",
                "action": (
                    "Convert suitable empty areas into pocket gardens, "
                    "seating areas, or shaded community spaces."
                ),
                "impact": (
                    "Better land use, increased greenery, "
                    "and improved community experience."
                ),
                "priority": "Medium",
            }
        )

    recommendations.append(
        {
            "title": "Evaluate solar-ready surfaces",
            "action": (
                "Review suitable rooftops and parking shade structures "
                "for potential solar-panel installation."
            ),
            "impact": (
                "Improved renewable-energy use and additional shaded surfaces."
            ),
            "priority": "Medium",
        }
    )

    return recommendations


def generate_summary(
    vision_result: dict,
    scores: dict,
) -> str:
    scene_type = vision_result.get("scene_type", "urban scene")
    heat_risk = scores["heat_risk"]

    if heat_risk == "High":
        condition = (
            "The scene has significant improvement potential, especially in "
            "shade, greenery, and pedestrian comfort."
        )

    elif heat_risk == "Medium":
        condition = (
            "The scene has moderate urban quality, with several opportunities "
            "to improve shade, greenery, and walkability."
        )

    else:
        condition = (
            "The scene has generally positive urban conditions, with opportunities "
            "for targeted sustainability improvements."
        )

    return (
        f"The uploaded image appears to show a {scene_type.lower()}. "
        f"{condition} The strongest visible improvements would come from native "
        "planting, shaded pedestrian routes, safer walking infrastructure, "
        "and better use of available open spaces."
    )
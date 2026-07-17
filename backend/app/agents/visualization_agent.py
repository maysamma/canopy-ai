from __future__ import annotations

from typing import Any


class VisualizationAgent:
    """
    Builds a realistic image-generation prompt from the urban analysis result.
    This version only prepares the prompt.
    The actual image-generation API will be connected in the next step.
    """

    def build_prompt(self, analysis: dict[str, Any]) -> str:
        scene = analysis.get("scene", {})
        scores = analysis.get("scores", {})
        recommendations = analysis.get("recommendations", [])

        scene_type = scene.get("scene_type", "urban street")
        trees = scene.get("trees", "unknown")
        sidewalk = scene.get("sidewalk", "unknown")
        road = scene.get("road", "unknown")
        buildings = scene.get("buildings", "unknown")
        empty_spaces = scene.get("empty_spaces", "unknown")
        shade = scene.get("shade", "unknown")

        heat_risk = scores.get("heat_risk", "unknown")

        recommendation_text = self._format_recommendations(recommendations)

        return f"""
Create a realistic improved version of the uploaded {scene_type} image.

Preserve the original:
- Buildings and architectural identity
- Road alignment and general street layout
- Camera angle and perspective
- Existing urban context

Current visible conditions:
- Trees: {trees}
- Sidewalk: {sidewalk}
- Road: {road}
- Buildings: {buildings}
- Empty spaces: {empty_spaces}
- Shade: {shade}
- Heat risk: {heat_risk}

Apply these urban improvements:
{recommendation_text}

Additional design requirements:
- Add native, drought-tolerant trees suitable for Saudi cities
- Improve pedestrian shade
- Add safe and continuous walking paths where possible
- Use realistic landscaping
- Keep vehicle access practical
- Avoid futuristic or unrealistic architecture
- Maintain natural daylight and realistic materials
- Produce a professional urban-design visualization
- Do not add text, labels, watermarks, logos, or diagrams

The final image should look like a realistic after-development photograph of the same location.
""".strip()

    @staticmethod
    def _format_recommendations(
        recommendations: list[dict[str, Any]],
    ) -> str:
        if not recommendations:
            return (
                "- Add native trees\n"
                "- Improve pedestrian shade\n"
                "- Improve walkability\n"
                "- Use available empty spaces for landscaping"
            )

        lines: list[str] = []

        for recommendation in recommendations:
            title = recommendation.get("title", "Urban improvement")
            action = recommendation.get("action", "")
            priority = recommendation.get("priority", "Medium")

            lines.append(
                f"- {title} ({priority} priority): {action}"
            )

        return "\n".join(lines)
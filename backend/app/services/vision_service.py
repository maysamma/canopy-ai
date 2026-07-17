from pathlib import Path

from app.agents.vision_agent import VisionAgent


_vision_agent: VisionAgent | None = None


def get_vision_agent() -> VisionAgent:
    global _vision_agent

    if _vision_agent is None:
        _vision_agent = VisionAgent()

    return _vision_agent


def analyze_image(
    image_path: str | Path,
) -> dict:
    agent = get_vision_agent()

    result = agent.analyze(image_path)

    return result.model_dump()
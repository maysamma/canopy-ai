from typing import Literal

from pydantic import BaseModel, Field


SceneType = Literal[
    "Urban Street",
    "Residential Street",
    "Commercial Street",
    "Public Space",
    "Parking Area",
    "Park",
    "Urban Area",
    "Non-Urban Scene",
]

Level = Literal[
    "none",
    "very few",
    "few",
    "some",
    "many",
    "unknown",
]

Visibility = Literal[
    "not visible",
    "limited",
    "partially visible",
    "visible",
    "prominent",
    "unknown",
]

SidewalkStatus = Literal[
    "not available",
    "limited",
    "partially available",
    "available",
    "wide",
    "unknown",
]

ShadeLevel = Literal[
    "none",
    "very low",
    "low",
    "medium",
    "high",
    "unknown",
]

EmptySpaceStatus = Literal[
    "not available",
    "limited",
    "available",
    "large",
    "unknown",
]


class VisionAnalysis(BaseModel):
    scene_type: SceneType

    trees: Level
    buildings: Visibility
    road: Visibility
    sidewalk: SidewalkStatus
    vehicles: Level
    shade: ShadeLevel
    empty_spaces: EmptySpaceStatus

    confidence: float = Field(
        ge=0.0,
        le=1.0,
        description=(
            "Overall confidence in the visible urban scene assessment."
        ),
    )
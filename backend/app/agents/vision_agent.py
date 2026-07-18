import os
from pathlib import Path

from dotenv import load_dotenv
from google import genai
from google.genai import types
from PIL import Image, UnidentifiedImageError

from app.schemas.vision import VisionAnalysis


load_dotenv(override=True)


VISION_PROMPT = """
You are the Vision Agent for Canopy AI, an AI-powered urban improvement
assistant for streets, neighborhoods, and public spaces.

Analyze the uploaded image using only visible evidence.

Your task is to describe the current scene accurately and conservatively.

Assess the following:

1. Scene type
   - Identify whether the image shows an urban street, residential area,
     commercial area, public space, parking area, park, highway, rural road,
     desert road, or another visible scene type.

2. Trees and vegetation
   - Describe whether vegetation is absent, sparse, moderate, or abundant.
   - Do not estimate exact percentages or exact numbers unless clearly visible.

3. Buildings
   - Describe whether buildings are visible.
   - Describe their general presence only, without guessing their use,
     ownership, age, structural condition, or compliance.

4. Road
   - State whether a road is visible.
   - Describe only clearly visible characteristics such as paved, unpaved,
     narrow, wide, divided, or unclear.

5. Sidewalk
   - State whether a sidewalk is visibly present, absent, partial, or unclear.
   - Do not assume that a road shoulder is a sidewalk.

6. Vehicles
   - State whether vehicles are visibly present.
   - Do not infer traffic volume from a single image.

7. Pedestrian shade
   - Assess only visible shade from trees, buildings, canopies, or structures.
   - Do not infer shade at other times of day.

8. Empty or underused space
   - Identify only clearly visible vacant, unused, or potentially underused
     areas.
   - Do not classify natural desert or undeveloped land as underused unless
     the scene clearly supports that conclusion.

Critical rules:

- Base every field only on what is visible in the image.
- Do not invent measurements, dimensions, temperatures, exact counts,
  locations, land use, building functions, or municipal information.
- Do not assume the scene is urban when the image is rural, desert,
  highway-based, or non-urban.
- Use "unknown" or the schema-equivalent value when evidence is insufficient.
- Do not generate recommendations.
- Do not generate issues.
- Do not calculate scores.
- Do not describe possible future improvements.
- Avoid contradictory values between fields.
- Confidence must reflect the overall reliability of the visual observations.
- Lower confidence when the image is blurry, distant, obstructed, dark,
  cropped, or does not clearly show the relevant elements.
- Return values that exactly match the provided response schema.
- Return only the structured response required by the schema.
"""


class VisionAgent:
    """
    Gemini-powered vision agent for urban scene analysis.
    """

    def __init__(self) -> None:
        api_key = os.getenv("GEMINI_API_KEY")

        if not api_key:
            raise RuntimeError(
                "GEMINI_API_KEY is missing. Add it to backend/.env."
            )

        self.model = os.getenv(
            "GEMINI_MODEL",
            "gemini-2.5-flash",
        )

        self.client = genai.Client(api_key=api_key)

    def analyze(
        self,
        image_path: str | Path,
    ) -> VisionAnalysis:
        path = Path(image_path)

        self._validate_image_path(path)

        try:
            with Image.open(path) as image:
                image.load()
                rgb_image = image.convert("RGB")

        except UnidentifiedImageError as error:
            raise ValueError(
                "The uploaded file is not a valid image."
            ) from error

        except OSError as error:
            raise ValueError(
                "The uploaded image could not be opened."
            ) from error

        try:
            response = self.client.models.generate_content(
                model=self.model,
                contents=[
                    VISION_PROMPT,
                    rgb_image,
                ],
                config=types.GenerateContentConfig(
                    temperature=0.1,
                    response_mime_type="application/json",
                    response_schema=VisionAnalysis,
                ),
            )

        except Exception as error:
            print("\n========== GEMINI VISION ERROR ==========")
            print(f"Error type: {type(error).__name__}")
            print(f"Error message: {error}")
            print("=========================================\n")

            raise RuntimeError(
                "Gemini Vision analysis failed."
            ) from error

        return self._parse_response(response)

    @staticmethod
    def _validate_image_path(path: Path) -> None:
        if not path.exists():
            raise FileNotFoundError(
                f"Image was not found: {path}"
            )

        if not path.is_file():
            raise ValueError(
                f"The supplied image path is not a file: {path}"
            )

        if path.suffix.lower() not in {
            ".jpg",
            ".jpeg",
            ".png",
            ".webp",
        }:
            raise ValueError(
                "Only JPG, JPEG, PNG, and WEBP images are supported."
            )

        if path.stat().st_size == 0:
            raise ValueError(
                "The uploaded image is empty."
            )

    @staticmethod
    def _parse_response(response) -> VisionAnalysis:
        if getattr(response, "parsed", None) is not None:
            parsed = response.parsed

            if isinstance(parsed, VisionAnalysis):
                return parsed

            return VisionAnalysis.model_validate(parsed)

        response_text = getattr(response, "text", None)

        if not response_text:
            raise RuntimeError(
                "Gemini returned an empty analysis."
            )

        try:
            return VisionAnalysis.model_validate_json(
                response_text
            )

        except Exception as error:
            print("Invalid Gemini JSON response:")
            print(response_text)

            raise RuntimeError(
                "Gemini returned an invalid structured response."
            ) from error
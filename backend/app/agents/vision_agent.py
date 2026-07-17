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
assistant.

Analyze the uploaded image as an urban planning scene.

Assess only what is visibly present in the image:

1. Scene type
2. Trees and vegetation
3. Buildings
4. Road visibility
5. Sidewalk availability
6. Vehicle presence
7. Pedestrian shade
8. Empty or underused spaces

Important rules:

- Base the analysis only on visible evidence.
- Do not invent measurements, temperatures, dimensions, or exact counts.
- Use "unknown" when the image does not provide enough evidence.
- Do not generate recommendations.
- Do not generate issues.
- Do not calculate scores.
- Do not claim professional engineering or municipal accuracy.
- Confidence must represent overall confidence in the visual analysis.
- Return values that exactly match the provided response schema.
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
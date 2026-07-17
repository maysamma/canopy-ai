from __future__ import annotations

import os
from pathlib import Path

from dotenv import load_dotenv
from google import genai
from google.genai import types
from PIL import Image

from google.genai import errors


load_dotenv()


GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GEMINI_IMAGE_MODEL = os.getenv(
    "GEMINI_IMAGE_MODEL",
    "gemini-3.1-flash-image",
)
GENERATED_DIR = Path(
    os.getenv("GENERATED_DIR", "generated")
)


def generate_improved_image(
    source_image_path: Path,
    prompt: str,
    project_id: str,
) -> Path:
    """
    Generate an improved version of the uploaded urban image.

    Returns the local path of the generated image.
    """

    if not GEMINI_API_KEY:
        raise RuntimeError(
            "GEMINI_API_KEY is missing from the environment."
        )

    if not source_image_path.exists():
        raise FileNotFoundError(
            f"Source image was not found: {source_image_path}"
        )

    GENERATED_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    client = genai.Client(
        api_key=GEMINI_API_KEY,
    )

    with Image.open(source_image_path) as image:
        source_image = image.convert("RGB")

        try:
            response = client.models.generate_content(
                model=GEMINI_IMAGE_MODEL,
                contents=[
                    prompt,
                    source_image,
                ],
                config=types.GenerateContentConfig(
                    response_modalities=[
                        "TEXT",
                        "IMAGE",
                    ],
                ),
            )

        except errors.ClientError as error:
            if error.code == 429:
                raise RuntimeError(
                    "Image generation quota is unavailable for the current Gemini API plan."
                ) from error

            raise RuntimeError(
                f"Gemini image generation failed: {error}"
            ) from error

    generated_image = None

    if not response.candidates:
        raise RuntimeError(
            "Gemini returned no image-generation candidates."
        )

    candidate = response.candidates[0]

    if not candidate.content or not candidate.content.parts:
        raise RuntimeError(
            "Gemini returned an empty image-generation response."
        )

    for part in candidate.content.parts:
        if part.inline_data and part.inline_data.data:
            generated_image = part.as_image()
            break

    if generated_image is None:
        raise RuntimeError(
            "Gemini did not return a generated image."
        )

    output_path = GENERATED_DIR / f"{project_id}_after.png"

    generated_image.save(output_path)

    return output_path
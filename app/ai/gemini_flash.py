import os
import base64
from io import BytesIO

from google import genai
from huggingface_hub import InferenceClient
from dotenv import load_dotenv

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
HF_TOKEN = os.getenv("HF_TOKEN")


def generate_story(topic: str) -> str:

    # Try Gemini first
    if GEMINI_API_KEY:
        try:
            client = genai.Client(api_key=GEMINI_API_KEY)

            prompt = f"""
Create a short 5-panel comic story about:
{topic}

Use this format:

Panel 1:
Scene:
Dialogue:

Panel 2:
Scene:
Dialogue:

Panel 3:
Scene:
Dialogue:

Panel 4:
Scene:
Dialogue:

Panel 5:
Scene:
Dialogue:
"""

            response = client.models.generate_content(
                model="gemini-3.5-flash-lite",
                contents=prompt
            )

            return response.text

        except Exception:
            pass

    # Backup story if Gemini is unavailable
    return f"""Panel 1:
Scene: A boy discovers something unusual related to {topic}.
Dialogue: "What is this?"

Panel 2:
Scene: He carefully explores the mysterious discovery.
Dialogue: "This could be something special!"

Panel 3:
Scene: A magical event suddenly takes place.
Dialogue: "Wow! I can't believe it!"

Panel 4:
Scene: The boy uses his discovery to solve a problem.
Dialogue: "I know what I have to do."

Panel 5:
Scene: Everything returns to normal and the boy smiles.
Dialogue: "What an amazing adventure!"
"""


def generate_image(topic: str) -> str:

    if not HF_TOKEN:
        return ""

    try:
        client = InferenceClient(
            provider="auto",
            api_key=HF_TOKEN
        )

        prompt = f"""
Colorful 2D cartoon comic illustration about {topic}.
Clean comic-book style, expressive characters,
bright background, student-friendly.
No text, no captions, no speech bubbles,
no logos, no watermark.
"""

        image = client.text_to_image(
            prompt,
            model="black-forest-labs/FLUX.1-schnell"
        )

        buffer = BytesIO()
        image.save(buffer, format="PNG")

        return base64.b64encode(
            buffer.getvalue()
        ).decode("utf-8")

    except Exception:
        return ""
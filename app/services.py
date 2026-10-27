import os

from dotenv import load_dotenv
from google import genai
from google.genai.errors import APIError, APITimeoutError

load_dotenv()

MODEL_NAME = "gemini-3.5-flash-lite"


def generate_ai_response(
    prompt: str,
    temperature: float = 1.0
) -> dict:
    """Call Gemini synchronously and return a dictionary."""

    api_key = os.getenv("GEMINI_API_KEY")

    if not api_key:
        raise RuntimeError("GEMINI_API_KEY is not configured")

    client = genai.Client(
        api_key=api_key,
        http_options={"timeout": 10000}
    )

    response = client.models.generate_content(
        model=MODEL_NAME,
        contents=prompt,
        config={"temperature": temperature}
    )

    if not response.text:
        raise RuntimeError("The AI model returned an empty response")

    return {
        "response": response.text,
        "model": MODEL_NAME
    }
from google import genai

from app.config import GEMINI_API_KEY, GEMINI_MODEL

def generate_response(prompt: str) -> str:
    if not GEMINI_API_KEY:
        raise ValueError("GEMINI_API_KEY is missing in .env")

    if not GEMINI_MODEL:
        raise ValueError("GEMINI_MODEL is missing in .env")

    client = genai.Client(api_key=GEMINI_API_KEY)
    response = client.models.generate_content(
        model=GEMINI_MODEL,
        contents=prompt
    )

    if not response.text:
        raise ValueError("Gemini returned an empty response")

    return response.text

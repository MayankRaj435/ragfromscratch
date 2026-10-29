
from google import genai
from google.genai import types
from app.config import GEMINI_API_KEY

EMBEDDING_MODEL = "gemini-embedding-2"


def embed_texts(texts: list[str]) -> list[list[float]]:
    if not GEMINI_API_KEY:
        raise ValueError("GEMINI_API_KEY is missing in .env")

    if not texts:
        return []

    client = genai.Client(api_key=GEMINI_API_KEY)

    contents = [
        types.Content(
            parts=[types.Part.from_text(text=text)]
        )
        for text in texts
    ]

    response = client.models.embed_content(
        model=EMBEDDING_MODEL,
        contents=contents,
    )

    if not response.embeddings:
        raise ValueError("The embedding API returned no embeddings.")

    if len(response.embeddings) != len(texts):
        raise ValueError(
            f"Expected {len(texts)} embeddings, "
            f"but received {len(response.embeddings)}."
        )

    return [embedding.values for embedding in response.embeddings]

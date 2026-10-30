
import logging
from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from google.genai.errors import APIError

from app.services.gemini_services import generate_response
from app.guardrails.input_checks import validate_question
from app.core.harness import answer_question

app = FastAPI(title="RAG Guardrails App")

logger = logging.getLogger(__name__)
FRONTEND_DIR = Path(__file__).resolve().parent / "static"
app.mount("/static", StaticFiles(directory=FRONTEND_DIR), name="static")


@app.get("/")
def home():
    return FileResponse(FRONTEND_DIR / "index.html")


@app.get("/health")
def health_check():
    return {"status": "healthy"}


class GeminiRequest(BaseModel):
    prompt: str


class AskRequest(BaseModel):
    question: str


@app.post("/gemini-test")
def gemini_test(request: GeminiRequest):
    try:
        question = validate_question(request.prompt)
    except ValueError as error:
        raise HTTPException(
            status_code=400,
            detail=str(error)
        )

    answer = generate_response(question)

    return {"answer": answer}


@app.post("/ask")
def ask(request: AskRequest):
    try:
        result = answer_question(request.question)
        return result

    except ValueError as error:
        raise HTTPException(
            status_code=400,
            detail=str(error)
        )

    except APIError as error:
        status_code = getattr(error, "code", 502)

        if status_code not in (429, 503):
            status_code = 502

        logger.warning("Gemini API request failed: %s", error)

        raise HTTPException(
            status_code=status_code,
            detail="The AI service is temporarily unavailable. Please retry."
        )

    except Exception:
        logger.exception("Unexpected RAG request failure")

        raise HTTPException(
            status_code=500,
            detail="An internal error occurred while processing the question."
        )

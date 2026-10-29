
from fastapi import FastAPI
from pydantic import BaseModel
from app.services.gemini_services import generate_response
from fastapi import HTTPException
from app.guardrails.input_checks import validate_question

app = FastAPI(title="RAG Guardrails App")


@app.get("/")
def home():
    return {
        "message": "RAG application is running",
        "status": "success"
    }


@app.get("/health")
def health_check():
    return {"status": "healthy"}

class GeminiRequest(BaseModel):
    prompt: str


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

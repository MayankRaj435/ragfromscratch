
from functools import lru_cache
from pathlib import Path

from app.guardrails.input_checks import validate_question
from app.rag.ingestion import read_document, split_into_chunks
from app.rag.embeddings import embed_texts
from app.rag.retrieval import retrieve_relevant_chunks
from app.rag.generation import generate_rag_answer


DOCUMENT_PATH = (
    Path(__file__).resolve().parents[2]
    / "data"
    / "documents"
    / "company_policy.txt"
)


@lru_cache(maxsize=1)
def load_document_index() -> tuple[list[str], list[list[float]]]:

    # 1. Read the document.
    document = read_document(str(DOCUMENT_PATH))

    # 2. Split the document into chunks.
    chunks = split_into_chunks(
        document,
        chunk_size=300,
        overlap=50,
    )

    if not chunks:
        return [], []

    # 3. Generate document embeddings only once.
    chunk_embeddings = embed_texts(chunks)

    return chunks, chunk_embeddings


def answer_question(question: str) -> dict:

    # 1. Validate the user's question.
    question = validate_question(question)

    # 2. Load the cached document index.
    chunks, chunk_embeddings = load_document_index()

    if not chunks:
        return {
            "answer": "No document content is available.",
            "sources": [],
        }

    # 3. Retrieve relevant chunks.
    results = retrieve_relevant_chunks(
        question=question,
        chunks=chunks,
        chunk_embeddings=chunk_embeddings,
        top_k=2,
    )

    context_chunks = [
        result["chunk"] for result in results
    ]

    # 4. Generate the answer.
    answer = generate_rag_answer(
        question=question,
        context_chunks=context_chunks,
    )

    # 5. Return answer and sources.
    return {
        "answer": answer,
        "sources": [
            {
                "text": result["chunk"],
                "score": round(result["score"], 4),
            }
            for result in results
        ],
    }

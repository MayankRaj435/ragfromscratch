
import math

from app.rag.embeddings import embed_texts


def cosine_similarity(
    vector_a: list[float],
    vector_b: list[float],
) -> float:
    if len(vector_a) != len(vector_b):
        raise ValueError("Vectors must have the same dimensions.")

    dot_product = sum(
        a * b for a, b in zip(vector_a, vector_b)
    )

    magnitude_a = math.sqrt(sum(a * a for a in vector_a))
    magnitude_b = math.sqrt(sum(b * b for b in vector_b))

    if magnitude_a == 0 or magnitude_b == 0:
        return 0.0

    return dot_product / (magnitude_a * magnitude_b)


def retrieve_relevant_chunks(
    question: str,
    chunks: list[str],
    chunk_embeddings: list[list[float]],
    top_k: int = 2,
) -> list[dict]:
    if len(chunks) != len(chunk_embeddings):
        raise ValueError("Each chunk must have one embedding.")

    if top_k <= 0:
        raise ValueError("top_k must be greater than zero.")

    if not chunks:
        return []

    question_embeddings = embed_texts([question])
    question_embedding = question_embeddings[0]

    scored_chunks = []

    for chunk, chunk_embedding in zip(chunks, chunk_embeddings):
        score = cosine_similarity(
            question_embedding,
            chunk_embedding,
        )

        scored_chunks.append({
            "chunk": chunk,
            "score": score,
        })

    scored_chunks.sort(
        key=lambda item: item["score"],
        reverse=True,
    )

    return scored_chunks[:top_k]


from app.rag.ingestion import read_document, split_into_chunks
from app.rag.embeddings import embed_texts
from app.rag.retrieval import retrieve_relevant_chunks
from app.rag.generation import generate_rag_answer

document = read_document("data/documents/company_policy.txt")

chunks = split_into_chunks(
    document,
    chunk_size=300,
    overlap=50,
)

chunk_embeddings = embed_texts(chunks)

question = "How many days of annual leave do employees receive?"

results = retrieve_relevant_chunks(
    question=question,
    chunks=chunks,
    chunk_embeddings=chunk_embeddings,
    top_k=2,
)

context_chunks = [
    result["chunk"] for result in results
]

answer = generate_rag_answer(
    question=question,
    context_chunks=context_chunks,
)

print("Question:", question)
print("\nRetrieved chunks:", len(context_chunks))

print("\nGenerated answer:")
print(answer)

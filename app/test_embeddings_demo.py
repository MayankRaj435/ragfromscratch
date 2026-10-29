
from app.rag.ingestion import read_document, split_into_chunks
from app.rag.embeddings import embed_texts

document = read_document("data/documents/company_policy.txt")

chunks = split_into_chunks(
    document,
    chunk_size=300,
    overlap=50,
)

embeddings = embed_texts(chunks)

print("Number of chunks:", len(chunks))
print("Number of embeddings:", len(embeddings))

for index, embedding in enumerate(embeddings):
    print(f"\nChunk {index + 1}")
    print("Vector dimensions:", len(embedding))
    print("First 5 values:", embedding[:5])

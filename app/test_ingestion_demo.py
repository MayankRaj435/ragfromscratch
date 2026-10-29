
from app.rag.ingestion import read_document, split_into_chunks


file_path = "data/documents/company_policy.txt"

document = read_document(file_path)

print("Original document length:", len(document))
print("\nOriginal document:")
print(document)

chunks = split_into_chunks(
    document,
    chunk_size=300,
    overlap=50,
)

print("\nNumber of chunks:", len(chunks))

for index, chunk in enumerate(chunks):
    print(f"\n--- Chunk {index + 1} ---")
    print("Characters:", len(chunk))
    print(chunk)


from app.core.harness import answer_question

question = "How many days of annual leave do employees receive?"

result = answer_question(question)

print("Question:", question)
print("\nAnswer:")
print(result["answer"])

print("\nSources:")
for source in result["sources"]:
    print("Similarity score:", source["score"])
    print(source["text"])
    print("-" * 40)

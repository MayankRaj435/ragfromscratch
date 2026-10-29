
MAX_QUESTION_LENGTH = 1000


def validate_question(question: str) -> str:
    if not question or not question.strip():
        raise ValueError("Question cannot be empty.")

    question = question.strip()

    if len(question) > MAX_QUESTION_LENGTH:
        raise ValueError(
            f"Question cannot exceed {MAX_QUESTION_LENGTH} characters."
        )

    return question

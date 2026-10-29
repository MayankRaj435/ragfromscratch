
import pytest

from app.guardrails.input_checks import validate_question


def test_valid_question():
    result = validate_question("What is RAG?")
    assert result == "What is RAG?"


def test_question_with_extra_spaces():
    result = validate_question("  What is RAG?  ")
    assert result == "What is RAG?"


def test_empty_question():
    with pytest.raises(ValueError):
        validate_question("")


def test_whitespace_only_question():
    with pytest.raises(ValueError):
        validate_question("   ")


def test_question_too_long():
    question = "a" * 1001

    with pytest.raises(ValueError):
        validate_question(question)

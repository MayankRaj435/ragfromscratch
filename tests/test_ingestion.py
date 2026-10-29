
import pytest

from app.rag.ingestion import split_into_chunks


def test_empty_text_returns_no_chunks():
    assert split_into_chunks("") == []


def test_short_text_returns_one_chunk():
    chunks = split_into_chunks("Hello RAG", chunk_size=20, overlap=5)

    assert chunks == ["Hello RAG"]


def test_chunks_respect_size_limit():
    text = "abcdefghijklmnopqrstuvwxyz"

    chunks = split_into_chunks(
        text,
        chunk_size=10,
        overlap=2,
    )

    assert all(len(chunk) <= 10 for chunk in chunks)


def test_chunks_overlap():
    text = "abcdefghijklmnopqrstuvwxyz"

    chunks = split_into_chunks(
        text,
        chunk_size=10,
        overlap=2,
    )

    assert chunks[0][-2:] == chunks[1][:2]


def test_invalid_overlap_is_rejected():
    with pytest.raises(ValueError):
        split_into_chunks("Hello world", chunk_size=10, overlap=10)


def test_invalid_chunk_size_is_rejected():
    with pytest.raises(ValueError):
        split_into_chunks("Hello world", chunk_size=0, overlap=0)

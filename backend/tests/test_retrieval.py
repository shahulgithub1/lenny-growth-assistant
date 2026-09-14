"""Tests for retrieval service."""
import pytest
from app.services.retrieval_service import RetrievalService


def test_retrieval_service_initialization():
    """Test retrieval service can be initialized."""
    service = RetrievalService()
    assert service is not None
    assert service.model_name == "sentence-transformers/all-MiniLM-L6-v2"


def test_generate_embedding():
    """Test embedding generation."""
    service = RetrievalService()
    embedding = service.generate_embedding("How to improve retention?")
    assert embedding is not None
    assert len(embedding) == 384  # MiniLM-L6-v2 dimension


def test_retrieve_chunks_without_index():
    """Test retrieval without FAISS index returns empty."""
    service = RetrievalService()
    results = service.retrieve_chunks("test query")
    # Should return empty list if index not loaded
    assert isinstance(results, list)

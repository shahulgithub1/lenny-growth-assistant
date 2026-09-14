"""Tests for LLM providers."""
import pytest
from app.services.llm_service import get_llm_provider, OllamaProvider, ConfigError
from app.core.config import settings


def test_get_ollama_provider():
    """Test getting Ollama provider."""
    provider = get_llm_provider("ollama")
    assert isinstance(provider, OllamaProvider)
    assert provider.model == settings.ollama_model


def test_provider_has_model_name():
    """Test provider returns model name."""
    provider = get_llm_provider("ollama")
    model_name = provider.get_model_name()
    assert model_name is not None
    assert len(model_name) > 0


def test_invalid_provider():
    """Test invalid provider raises error."""
    with pytest.raises(ConfigError):
        get_llm_provider("invalid_provider")

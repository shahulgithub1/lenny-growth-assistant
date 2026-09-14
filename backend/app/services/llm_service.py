"""LLM provider abstraction."""
from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional
import anthropic
import ollama

from app.core.config import settings
from app.core.logging import get_logger

logger = get_logger(__name__)


class LLMProvider(ABC):
    """Abstract LLM provider interface."""
    
    @abstractmethod
    def generate(
        self,
        messages: List[Dict[str, str]],
        max_tokens: int = 2000,
        temperature: float = 0.7,
        **kwargs
    ) -> Dict[str, Any]:
        """Generate completion from messages."""
        pass
    
    @abstractmethod
    def is_available(self) -> bool:
        """Check if provider is available."""
        pass
    
    @abstractmethod
    def get_model_name(self) -> str:
        """Get current model name."""
        pass


class OllamaProvider(LLMProvider):
    """Ollama provider implementation."""
    
    def __init__(self, base_url: str, model: str):
        self.base_url = base_url
        self.model = model
        self.client = ollama.Client(host=base_url)
        logger.info("ollama_provider_initialized", base_url=base_url, model=model)
    
    def generate(
        self,
        messages: List[Dict[str, str]],
        max_tokens: int = 2000,
        temperature: float = 0.7,
        **kwargs
    ) -> Dict[str, Any]:
        """Generate completion using Ollama."""
        try:
            logger.info("ollama_generation_requested", model=self.model, messages_count=len(messages))
            
            response = self.client.chat(
                model=self.model,
                messages=messages,
                options={
                    "temperature": temperature,
                    "num_predict": max_tokens
                }
            )
            
            content = response["message"]["content"]
            
            logger.info("ollama_generation_completed", response_length=len(content))
            
            return {
                "content": content,
                "model": self.model,
                "provider": "ollama"
            }
            
        except Exception as e:
            logger.error("ollama_generation_failed", error=str(e))
            raise LLMUnavailableError(f"Ollama unavailable: {str(e)}")
    
    def is_available(self) -> bool:
        """Check if Ollama is available."""
        try:
            self.client.list()
            return True
        except:
            return False
    
    def get_model_name(self) -> str:
        """Get model name."""
        return self.model


class AnthropicProvider(LLMProvider):
    """Anthropic provider implementation."""
    
    def __init__(self, api_key: str, model: str):
        self.api_key = api_key
        self.model = model
        self.client = anthropic.Anthropic(api_key=api_key)
        logger.info("anthropic_provider_initialized", model=model)
    
    def generate(
        self,
        messages: List[Dict[str, str]],
        max_tokens: int = 2000,
        temperature: float = 0.7,
        **kwargs
    ) -> Dict[str, Any]:
        """Generate completion using Anthropic."""
        try:
            logger.info("anthropic_generation_requested", model=self.model, messages_count=len(messages))
            
            # Extract system message if present
            system_message = None
            filtered_messages = []
            for msg in messages:
                if msg["role"] == "system":
                    system_message = msg["content"]
                else:
                    filtered_messages.append(msg)
            
            response = self.client.messages.create(
                model=self.model,
                max_tokens=max_tokens,
                temperature=temperature,
                system=system_message,
                messages=filtered_messages
            )
            
            content = response.content[0].text
            
            logger.info("anthropic_generation_completed", response_length=len(content))
            
            return {
                "content": content,
                "model": self.model,
                "provider": "anthropic",
                "usage": {
                    "input_tokens": response.usage.input_tokens,
                    "output_tokens": response.usage.output_tokens
                }
            }
            
        except anthropic.AuthenticationError as e:
            logger.error("anthropic_auth_failed", error=str(e))
            raise LLMAuthError("Invalid Anthropic API key")
        except Exception as e:
            logger.error("anthropic_generation_failed", error=str(e))
            raise LLMUnavailableError(f"Anthropic unavailable: {str(e)}")
    
    def is_available(self) -> bool:
        """Check if Anthropic is available."""
        return bool(self.api_key)
    
    def get_model_name(self) -> str:
        """Get model name."""
        return self.model


def get_llm_provider(provider_name: Optional[str] = None) -> LLMProvider:
    """Factory function to get LLM provider."""
    if provider_name is None:
        provider_name = settings.model_provider
    
    provider_name = provider_name.lower()
    
    if provider_name == "ollama":
        return OllamaProvider(
            base_url=settings.ollama_base_url,
            model=settings.ollama_model
        )
    elif provider_name == "anthropic":
        if not settings.anthropic_api_key:
            raise ConfigError("ANTHROPIC_API_KEY not set")
        return AnthropicProvider(
            api_key=settings.anthropic_api_key,
            model=settings.anthropic_model
        )
    else:
        raise ConfigError(f"Unknown provider: {provider_name}")


class LLMUnavailableError(Exception):
    """LLM service unavailable."""
    pass


class LLMAuthError(Exception):
    """LLM authentication error."""
    pass


class ConfigError(Exception):
    """Configuration error."""
    pass

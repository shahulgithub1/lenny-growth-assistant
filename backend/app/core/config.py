"""
Application configuration loaded from environment variables.
"""
from typing import Optional
from pydantic_settings import BaseSettings
from pydantic import Field


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""
    
    # Database
    database_url: str = Field(
        default="postgresql://lenny:lenny_dev_password@localhost:5432/lenny_growth_assistant",
        description="PostgreSQL database URL"
    )
    
    # Model Provider
    model_provider: str = Field(
        default="ollama",
        description="LLM provider: 'ollama' or 'anthropic'"
    )
    
    # Ollama Configuration
    ollama_base_url: str = Field(
        default="http://localhost:11434",
        description="Ollama API base URL"
    )
    ollama_model: str = Field(
        default="llama3.2:8b",
        description="Ollama model name"
    )
    
    # Anthropic Configuration
    anthropic_api_key: Optional[str] = Field(
        default=None,
        description="Anthropic API key (optional)"
    )
    anthropic_model: str = Field(
        default="claude-3-5-sonnet-20241022",
        description="Anthropic model name"
    )
    
    # Application
    backend_host: str = Field(default="0.0.0.0", description="Backend host")
    backend_port: int = Field(default=8000, description="Backend port")
    
    # Logging
    log_level: str = Field(default="INFO", description="Log level")
    
    # Retrieval
    retrieval_top_k: int = Field(default=5, description="Number of chunks to retrieve")
    retrieval_threshold: float = Field(default=0.7, description="Similarity threshold")
    
    class Config:
        case_sensitive = False
        extra = "ignore"  # Ignore extra env vars (e.g. Docker Compose vars)


# Global settings instance
settings = Settings()

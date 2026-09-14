"""
Main FastAPI application entry point.
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from app.core.config import settings
from app.core.logging import setup_logging, get_logger
from app.api.routes import health, sessions, artifacts

# Setup logging
setup_logging()
logger = get_logger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan events."""
    # Startup
    logger.info(
        "application_starting",
        model_provider=settings.model_provider,
        ollama_url=settings.ollama_base_url,
        ollama_model=settings.ollama_model,
    )
    yield
    # Shutdown
    logger.info("application_shutting_down")


# Create FastAPI application
app = FastAPI(
    title="The Lenny Growth Assistant API",
    description="AI-powered research assistant for product and growth teams",
    version="1.0.0",
    lifespan=lifespan,
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",  # Frontend dev server
        "http://localhost:3000",  # Alternative frontend port
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(health.router, tags=["Health"])
app.include_router(sessions.router, tags=["Sessions"])
app.include_router(artifacts.router, tags=["Artifacts"])

logger.info("fastapi_application_configured")

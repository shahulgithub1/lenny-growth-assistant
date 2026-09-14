"""
Health check endpoints.
"""
from fastapi import APIRouter, status
from datetime import datetime
from typing import Dict, Any

from app.core.logging import get_logger

logger = get_logger(__name__)
router = APIRouter()


@router.get("/health", status_code=status.HTTP_200_OK)
async def health_check() -> Dict[str, Any]:
    """
    Health check endpoint.
    
    Returns service health status and basic diagnostics.
    """
    logger.info("health_check_requested")
    
    response = {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "service": "lenny-growth-assistant",
        "version": "1.0.0"
    }
    
    logger.info("health_check_completed", status="healthy")
    return response

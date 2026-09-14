"""Artifact management routes."""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session as DBSession
from typing import List
from uuid import UUID

from app.db.session import get_db
from app.db.models import Artifact
from app.api.schemas.artifacts import ArtifactResponse
from app.core.logging import get_logger

logger = get_logger(__name__)
router = APIRouter(prefix="/api")


@router.get("/artifacts/{artifact_id}", response_model=ArtifactResponse)
def get_artifact(
    artifact_id: UUID,
    db: DBSession = Depends(get_db)
):
    """Get a specific artifact by ID."""
    logger.info("get_artifact_requested", artifact_id=str(artifact_id))
    
    artifact = db.query(Artifact).filter(Artifact.id == artifact_id).first()
    
    if not artifact:
        logger.warning("artifact_not_found", artifact_id=str(artifact_id))
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Artifact {artifact_id} not found"
        )
    
    return artifact


@router.get("/sessions/{session_id}/artifacts", response_model=List[ArtifactResponse])
def list_session_artifacts(
    session_id: UUID,
    db: DBSession = Depends(get_db)
):
    """List all artifacts for a session."""
    logger.info("list_artifacts_requested", session_id=str(session_id))
    
    artifacts = db.query(Artifact).filter(
        Artifact.session_id == session_id
    ).order_by(Artifact.created_at.desc()).all()
    
    return artifacts

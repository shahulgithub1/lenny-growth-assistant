"""Artifact schemas."""
from pydantic import BaseModel, Field
from uuid import UUID
from datetime import datetime
from typing import Optional, Dict, Any


class ArtifactMetadata(BaseModel):
    """Artifact metadata."""
    title: Optional[str] = None
    description: Optional[str] = None
    size_bytes: Optional[int] = None


class ArtifactResponse(BaseModel):
    """Artifact response schema."""
    id: UUID
    session_id: UUID
    message_id: Optional[UUID] = None
    type: str = Field(..., description="Artifact type: markdown, html, css")
    content: str
    created_at: datetime
    metadata: Optional[Dict[str, Any]] = Field(default=None, alias="artifact_metadata")
    
    class Config:
        from_attributes = True
        populate_by_name = True

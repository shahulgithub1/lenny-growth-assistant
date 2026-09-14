"""Session-related Pydantic schemas."""
from pydantic import BaseModel, Field, ConfigDict, field_serializer
from typing import Optional, List, Dict, Any
from datetime import datetime, timezone
from uuid import UUID


def ensure_utc_datetime(dt: datetime) -> datetime:
    """Ensure datetime is timezone-aware UTC."""
    if dt is None:
        return None
    if dt.tzinfo is None:
        # Naive datetime - assume UTC
        return dt.replace(tzinfo=timezone.utc)
    return dt


class Source(BaseModel):
    """Source citation schema."""
    episode_title: str
    guest: Optional[str] = None
    excerpt: str
    chunk_id: str
    source_file: str


class MessageCreate(BaseModel):
    """Message creation request."""
    content: str = Field(..., min_length=1, max_length=10000)
    model_provider: Optional[str] = None


class MessageResponse(BaseModel):
    """Message response."""
    model_config = ConfigDict(from_attributes=True, populate_by_name=True)
    
    id: UUID
    role: str
    content: str
    sources: Optional[List[Source]] = []
    created_at: datetime
    metadata: Optional[Dict[str, Any]] = Field(default={}, alias="message_metadata")
    
    @field_serializer('created_at')
    def serialize_created_at(self, dt: datetime) -> str:
        """Serialize datetime as UTC ISO 8601."""
        dt_utc = ensure_utc_datetime(dt)
        return dt_utc.isoformat()


class SessionCreate(BaseModel):
    """Session creation request."""
    title: Optional[str] = None


class SessionResponse(BaseModel):
    """Session response."""
    model_config = ConfigDict(from_attributes=True, populate_by_name=True)
    
    id: UUID
    created_at: datetime
    updated_at: datetime
    title: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = Field(default={}, alias="session_metadata")
    
    @field_serializer('created_at', 'updated_at')
    def serialize_datetime(self, dt: datetime) -> str:
        """Serialize datetime as UTC ISO 8601."""
        dt_utc = ensure_utc_datetime(dt)
        return dt_utc.isoformat()


class SessionDetail(BaseModel):
    """Detailed session with messages."""
    model_config = ConfigDict(from_attributes=True, populate_by_name=True)
    
    id: UUID
    created_at: datetime
    updated_at: datetime
    title: Optional[str] = None
    messages: List[MessageResponse]
    metadata: Optional[Dict[str, Any]] = Field(default={}, alias="session_metadata")
    
    @field_serializer('created_at', 'updated_at')
    def serialize_datetime(self, dt: datetime) -> str:
        """Serialize datetime as UTC ISO 8601."""
        dt_utc = ensure_utc_datetime(dt)
        return dt_utc.isoformat()


class SessionList(BaseModel):
    """List of sessions."""
    sessions: List[SessionResponse]
    total: int
    limit: int
    offset: int


class ErrorResponse(BaseModel):
    """Error response."""
    error: str
    message: str
    details: Optional[Dict[str, Any]] = None
    request_id: Optional[str] = None

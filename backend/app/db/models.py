"""SQLAlchemy models."""
from sqlalchemy import Column, String, Text, Integer, DateTime, ForeignKey, JSON, TypeDecorator, CHAR
from sqlalchemy.dialects.postgresql import UUID as PostgreSQL_UUID
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
import uuid

Base = declarative_base()


def utcnow():
    """Get current UTC time with timezone awareness."""
    return datetime.now(timezone.utc)


class UUID(TypeDecorator):
    """Platform-independent UUID type.
    
    Uses PostgreSQL's UUID type, otherwise uses CHAR(36),
    storing as stringified hex values.
    """
    impl = CHAR
    cache_ok = True

    def __init__(self, as_uuid=True):
        """Initialize UUID type.
        
        Args:
            as_uuid: Whether to return UUID objects (True) or strings (False).
                    This parameter is kept for API compatibility but the type
                    always returns uuid.UUID objects in Python.
        """
        super().__init__()
        self.as_uuid = as_uuid

    def load_dialect_impl(self, dialect):
        if dialect.name == 'postgresql':
            return dialect.type_descriptor(PostgreSQL_UUID(as_uuid=True))
        else:
            return dialect.type_descriptor(CHAR(36))

    def process_bind_param(self, value, dialect):
        if value is None:
            return value
        elif dialect.name == 'postgresql':
            return value
        else:
            if not isinstance(value, uuid.UUID):
                return str(uuid.UUID(value))
            else:
                return str(value)

    def process_result_value(self, value, dialect):
        if value is None:
            return value
        if not isinstance(value, uuid.UUID):
            return uuid.UUID(value)
        return value


class Session(Base):
    """Chat session model."""
    __tablename__ = "sessions"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    created_at = Column(DateTime(timezone=True), default=utcnow, nullable=False)
    updated_at = Column(DateTime(timezone=True), default=utcnow, onupdate=utcnow, nullable=False)
    title = Column(String(255), nullable=True)
    session_metadata = Column("metadata", JSON, nullable=True)
    
    messages = relationship("Message", back_populates="session", cascade="all, delete-orphan")
    artifacts = relationship("Artifact", back_populates="session", cascade="all, delete-orphan")


class Message(Base):
    """Message model."""
    __tablename__ = "messages"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    session_id = Column(UUID(as_uuid=True), ForeignKey("sessions.id", ondelete="CASCADE"), nullable=False)
    role = Column(String(20), nullable=False)
    content = Column(Text, nullable=False)
    sources = Column(JSON, nullable=True)
    created_at = Column(DateTime(timezone=True), default=utcnow, nullable=False)
    message_metadata = Column("metadata", JSON, nullable=True)
    
    session = relationship("Session", back_populates="messages")


class Artifact(Base):
    """Artifact model."""
    __tablename__ = "artifacts"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    session_id = Column(UUID(as_uuid=True), ForeignKey("sessions.id", ondelete="CASCADE"), nullable=False)
    message_id = Column(UUID(as_uuid=True), ForeignKey("messages.id", ondelete="CASCADE"), nullable=True)
    type = Column(String(20), nullable=False)
    content = Column(Text, nullable=False)
    created_at = Column(DateTime(timezone=True), default=utcnow, nullable=False)
    artifact_metadata = Column("metadata", JSON, nullable=True)
    
    session = relationship("Session", back_populates="artifacts")


class TranscriptChunk(Base):
    """Transcript chunk model."""
    __tablename__ = "transcript_chunks"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    episode_title = Column(String(500), nullable=True)
    guest = Column(String(255), nullable=True)
    source_file = Column(String(500), nullable=False)
    chunk_index = Column(Integer, nullable=False)
    content = Column(Text, nullable=False)
    created_at = Column(DateTime(timezone=True), default=utcnow, nullable=False)
    chunk_metadata = Column("metadata", JSON, nullable=True)

"""Session management routes."""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session as DBSession
from typing import List
from uuid import UUID
import re

from app.db.session import get_db
from app.db.models import Session, Message, Artifact
from app.api.schemas.sessions import (
    SessionCreate, SessionResponse, SessionDetail, SessionList, 
    MessageCreate, MessageResponse
)
from app.services.agent_service import AgentService
from app.core.logging import get_logger

logger = get_logger(__name__)
router = APIRouter(prefix="/api")


@router.post("/sessions", response_model=SessionResponse, status_code=status.HTTP_201_CREATED)
def create_session(
    session_data: SessionCreate,
    db: DBSession = Depends(get_db)
):
    """Create a new chat session."""
    logger.info("create_session_requested", title=session_data.title)
    
    session = Session(title=session_data.title)
    db.add(session)
    db.commit()
    db.refresh(session)
    
    logger.info("session_created", session_id=str(session.id))
    return session


@router.get("/sessions", response_model=SessionList)
def list_sessions(
    limit: int = 50,
    offset: int = 0,
    db: DBSession = Depends(get_db)
):
    """List all sessions."""
    logger.info("list_sessions_requested", limit=limit, offset=offset)
    
    total = db.query(Session).count()
    sessions = db.query(Session).order_by(Session.created_at.desc()).limit(limit).offset(offset).all()
    
    return SessionList(sessions=sessions, total=total, limit=limit, offset=offset)


@router.get("/sessions/{session_id}", response_model=SessionDetail)
def get_session(
    session_id: UUID,
    db: DBSession = Depends(get_db)
):
    """Get a specific session with messages."""
    logger.info("get_session_requested", session_id=str(session_id))
    
    session = db.query(Session).filter(Session.id == session_id).first()
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    
    messages = db.query(Message).filter(Message.session_id == session_id).order_by(Message.created_at).all()
    
    return SessionDetail(
        id=session.id,
        created_at=session.created_at,
        updated_at=session.updated_at,
        title=session.title,
        messages=messages,
        metadata=session.session_metadata or {}
    )


@router.delete("/sessions/{session_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_session(
    session_id: UUID,
    db: DBSession = Depends(get_db)
):
    """Delete a session and all associated messages and artifacts."""
    logger.info("delete_session_requested", session_id=str(session_id))
    
    session = db.query(Session).filter(Session.id == session_id).first()
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    
    # Delete session (cascade will handle messages and artifacts)
    db.delete(session)
    db.commit()
    
    logger.info("session_deleted", session_id=str(session_id))
    return None


@router.post("/sessions/{session_id}/messages", response_model=MessageResponse)
async def send_message(
    session_id: UUID,
    message_data: MessageCreate,
    db: DBSession = Depends(get_db)
):
    """Send a message and get AI response."""
    logger.info("send_message_requested", session_id=str(session_id), content_length=len(message_data.content))
    
    # Verify session exists
    session = db.query(Session).filter(Session.id == session_id).first()
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    
    # Store user message
    user_message = Message(
        session_id=session_id,
        role="user",
        content=message_data.content
    )
    db.add(user_message)
    db.commit()
    
    # Get conversation history
    messages = db.query(Message).filter(Message.session_id == session_id).order_by(Message.created_at).all()
    
    # Generate AI response
    agent_service = AgentService(db)
    response = await agent_service.generate_response(
        session_id=session_id,
        user_message=message_data.content,
        conversation_history=messages,
        model_provider=message_data.model_provider
    )
    
    # Store assistant message
    assistant_message = Message(
        session_id=session_id,
        role="assistant",
        content=response["content"],
        sources=response.get("sources"),
        message_metadata=response.get("metadata")
    )
    db.add(assistant_message)
    db.flush()  # Get message ID before detecting artifacts
    
    # Detect and persist artifacts
    skill = response.get("metadata", {}).get("skill")
    if skill == "artifact":
        artifact_type, artifact_content = _extract_artifact(response["content"])
        if artifact_content:
            logger.info("artifact_detected", type=artifact_type)
            artifact = Artifact(
                session_id=session_id,
                message_id=assistant_message.id,
                type=artifact_type,
                content=artifact_content,
                artifact_metadata={
                    "title": _extract_artifact_title(response["content"]),
                    "size_bytes": len(artifact_content)
                }
            )
            db.add(artifact)
            db.flush()

            # Update assistant message metadata with artifact reference
            if assistant_message.message_metadata is None:
                assistant_message.message_metadata = {}
            assistant_message.message_metadata = {
                **assistant_message.message_metadata,
                "artifact_id": str(artifact.id)
            }

    # Update session timestamp
    session.updated_at = assistant_message.created_at
    if not session.title and len(messages) == 1:
        # Set title from first message
        session.title = message_data.content[:100]
    
    db.commit()
    db.refresh(assistant_message)
    
    logger.info("message_generated", session_id=str(session_id), message_id=str(assistant_message.id))
    
    return assistant_message


def _extract_artifact(content: str) -> tuple[str, str | None]:
    """Extract artifact type and content from assistant response."""
    # Check for HTML artifact
    if "<!DOCTYPE html>" in content or "<html>" in content:
        # Extract HTML content
        html_match = re.search(r'<!DOCTYPE html>.*?</html>', content, re.DOTALL | re.IGNORECASE)
        if html_match:
            return "html", html_match.group(0)
        
        html_match = re.search(r'<html.*?>.*?</html>', content, re.DOTALL | re.IGNORECASE)
        if html_match:
            return "html", html_match.group(0)
    
    # Markdown fallback: any substantial text routed to the artifact skill
    if len(content) > 100:
        return "markdown", content

    return "markdown", None


def _extract_artifact_title(content: str) -> str:
    """Extract title from artifact content."""
    # Try to find first heading
    heading_match = re.search(r'^#\s+(.+)$', content, re.MULTILINE)
    if heading_match:
        return heading_match.group(1).strip()
    
    # Try HTML title
    title_match = re.search(r'<title>(.+?)</title>', content, re.IGNORECASE)
    if title_match:
        return title_match.group(1).strip()
    
    return "Untitled Artifact"

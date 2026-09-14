"""Database session management."""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session as SQLSession
from contextlib import contextmanager
from typing import Generator

from app.core.config import settings

engine = create_engine(settings.database_url, pool_pre_ping=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db() -> Generator[SQLSession, None, None]:
    """Dependency for database session."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@contextmanager
def get_db_context():
    """Context manager for database session."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

"""
Lenny transcript ingestion script.

Loads transcripts from GitHub repo, chunks them, generates embeddings,
and builds FAISS index.
"""
import os
import sys
import re
import json
import subprocess
import yaml
from pathlib import Path
from typing import List, Dict, Any
import numpy as np
import faiss
from sentence_transformers import SentenceTransformer
from sqlalchemy.orm import Session

# Add backend to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "backend"))

from app.db.models import TranscriptChunk, Base
from app.db.session import engine, get_db_context
from app.core.logging import setup_logging, get_logger

setup_logging()
logger = get_logger(__name__)

TRANSCRIPT_REPO = "https://github.com/ChatPRD/lennys-podcast-transcripts.git"
DATA_DIR = Path(__file__).parent.parent / "data"
TRANSCRIPTS_DIR = DATA_DIR / "transcripts"
BACKEND_DATA_DIR = Path(__file__).parent.parent.parent / "backend" / "data"

CHUNK_SIZE = 500  # tokens
OVERLAP = 50  # tokens
MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"


def clone_or_update_repo():
    """Clone or update transcript repository."""
    logger.info("cloning_transcript_repo", repo=TRANSCRIPT_REPO)
    
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    
    if TRANSCRIPTS_DIR.exists():
        logger.info("repository_exists_pulling_updates")
        subprocess.run(["git", "-C", str(TRANSCRIPTS_DIR), "pull"], check=True)
    else:
        logger.info("cloning_repository")
        subprocess.run(["git", "clone", TRANSCRIPT_REPO, str(TRANSCRIPTS_DIR)], check=True)
    
    logger.info("repository_ready")


def extract_metadata(file_path: Path, content: str) -> Dict[str, Any]:
    """Extract episode title and guest from directory path and frontmatter using proper YAML parsing."""
    metadata = {
        "episode_title": None,
        "guest": None
    }
    
    # Extract from directory name (e.g., episodes/casey-winters/transcript.md)
    parts = file_path.parts
    if 'episodes' in parts:
        episode_idx = parts.index('episodes')
        if episode_idx + 1 < len(parts):
            # Convert directory name to title case as fallback
            guest_slug = parts[episode_idx + 1]
            guest_name = guest_slug.replace('-', ' ').replace('_', ' ').title()
            metadata["episode_title"] = guest_name
            metadata["guest"] = guest_name
    
    # Parse frontmatter using PyYAML
    if content.startswith('---'):
        try:
            end_idx = content.find('---', 3)
            if end_idx > 0:
                frontmatter_str = content[3:end_idx].strip()
                frontmatter = yaml.safe_load(frontmatter_str)
                
                if isinstance(frontmatter, dict):
                    # Extract guest field
                    if 'guest' in frontmatter and frontmatter['guest']:
                        guest = str(frontmatter['guest']).strip()
                        metadata["guest"] = guest[:255]  # Limit to 255 chars for DB
                    
                    # Extract title field
                    if 'title' in frontmatter and frontmatter['title']:
                        title = str(frontmatter['title']).strip()
                        # Remove everything after | if present (usually contains guest info)
                        if '|' in title:
                            title = title.split('|')[0].strip()
                        metadata["episode_title"] = title[:255]  # Limit to 255 chars for DB
        except yaml.YAMLError as e:
            logger.warning("yaml_parse_error", file=str(file_path), error=str(e))
        except Exception as e:
            logger.warning("metadata_extract_error", file=str(file_path), error=str(e))
    
    # Fallback: use filename if no metadata found
    if not metadata["episode_title"]:
        metadata["episode_title"] = file_path.stem
    if not metadata["guest"]:
        metadata["guest"] = "Unknown"
    
    # Ensure we have reasonable defaults
    if not metadata["guest"] and metadata["episode_title"]:
        metadata["guest"] = metadata["episode_title"]
    
    return metadata


def chunk_text(text: str, chunk_size: int = CHUNK_SIZE, overlap: int = OVERLAP) -> List[str]:
    """Chunk text with sliding window and overlap."""
    # Simple word-based chunking
    words = text.split()
    chunks = []
    
    i = 0
    while i < len(words):
        chunk = ' '.join(words[i:i + chunk_size])
        chunks.append(chunk)
        i += chunk_size - overlap
        
        if i >= len(words):
            break
    
    logger.debug("text_chunked", total_chunks=len(chunks))
    return chunks


def load_transcripts() -> List[Dict[str, Any]]:
    """Load and process all transcript files."""
    logger.info("loading_transcripts", dir=str(TRANSCRIPTS_DIR))
    
    transcripts = []
    
    # Only load transcript files from episode directories
    # Pattern: transcripts/episodes/*/transcript.md
    episodes_dir = TRANSCRIPTS_DIR / "episodes"
    if not episodes_dir.exists():
        logger.error("episodes_directory_not_found", path=str(episodes_dir))
        return transcripts
    
    transcript_files = list(episodes_dir.glob("*/transcript.md")) + list(episodes_dir.glob("*/transcript.txt"))
    
    logger.info("found_transcript_files", count=len(transcript_files))
    
    for file_path in transcript_files:
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                original_content = f.read()
            
            # Skip if content is too short (likely not a real transcript)
            if len(original_content) < 500:
                logger.warning("skipping_short_file", file=str(file_path), length=len(original_content))
                continue
            
            # Extract metadata from ORIGINAL content (before cleaning)
            metadata = extract_metadata(file_path, original_content)
            
            # Remove frontmatter from content before chunking
            content = original_content
            if content.startswith('---'):
                end_idx = content.find('---', 3)
                if end_idx > 0:
                    content = content[end_idx + 3:].strip()
            
            # Clean content for chunking
            content = re.sub(r'\s+', ' ', content)  # Normalize whitespace
            content = re.sub(r'\[.*?\]', '', content)  # Remove timestamps like [00:12:34]
            
            chunks = chunk_text(content)
            
            # Get relative path from transcripts directory
            relative_path = file_path.relative_to(TRANSCRIPTS_DIR)
            
            for idx, chunk in enumerate(chunks):
                transcripts.append({
                    "source_file": str(relative_path),  # Store full relative path
                    "chunk_index": idx,
                    "content": chunk,
                    "episode_title": metadata["episode_title"],
                    "guest": metadata["guest"],
                    "episode_path": file_path.parent.name  # Store directory name for reference
                })
            
            logger.debug("transcript_processed", file=file_path.name, chunks=len(chunks))
        
        except Exception as e:
            logger.error("transcript_load_failed", file=str(file_path), error=str(e))
    
    logger.info("transcripts_loaded", total_chunks=len(transcripts))
    return transcripts


def generate_embeddings(transcripts: List[Dict[str, Any]]) -> np.ndarray:
    """Generate embeddings for all chunks."""
    logger.info("loading_embedding_model", model=MODEL_NAME)
    model = SentenceTransformer(MODEL_NAME)
    
    texts = [t["content"] for t in transcripts]
    logger.info("generating_embeddings", count=len(texts))
    
    embeddings = model.encode(texts, show_progress_bar=True, batch_size=32)
    
    logger.info("embeddings_generated", shape=embeddings.shape)
    return embeddings.astype('float32')


def build_faiss_index(embeddings: np.ndarray) -> faiss.Index:
    """Build FAISS index from embeddings."""
    logger.info("building_faiss_index", dimensions=embeddings.shape[1])
    
    # Use flat L2 index for simplicity and accuracy
    index = faiss.IndexFlatL2(embeddings.shape[1])
    index.add(embeddings)
    
    logger.info("faiss_index_built", total_vectors=index.ntotal)
    return index


def save_index_and_mapping(index: faiss.Index, transcripts: List[Dict[str, Any]]):
    """Save FAISS index and chunk mapping."""
    BACKEND_DATA_DIR.mkdir(parents=True, exist_ok=True)
    
    index_path = BACKEND_DATA_DIR / "faiss_index.bin"
    mapping_path = BACKEND_DATA_DIR / "chunk_mapping.json"
    
    logger.info("saving_faiss_index", path=str(index_path))
    faiss.write_index(index, str(index_path))
    
    # Create chunk mapping (chunk_idx -> metadata)
    chunk_mapping = {}
    for idx, transcript in enumerate(transcripts):
        chunk_mapping[str(idx)] = {
            "episode_title": transcript["episode_title"],
            "guest": transcript["guest"],
            "content": transcript["content"],
            "source_file": transcript["source_file"],
            "chunk_index": transcript["chunk_index"],
            "episode_path": transcript.get("episode_path", "")
        }
    
    logger.info("saving_chunk_mapping", path=str(mapping_path), chunks=len(chunk_mapping))
    with open(mapping_path, 'w') as f:
        json.dump(chunk_mapping, f)
    
    logger.info("index_and_mapping_saved")


def store_chunks_in_db(transcripts: List[Dict[str, Any]]):
    """Store chunks in PostgreSQL."""
    logger.info("storing_chunks_in_database", count=len(transcripts))
    
    # Create tables
    Base.metadata.create_all(bind=engine)
    
    with get_db_context() as db:
        # Clear existing chunks
        db.query(TranscriptChunk).delete()
        
        # Insert new chunks
        for transcript in transcripts:
            chunk = TranscriptChunk(
                episode_title=transcript["episode_title"],
                guest=transcript["guest"],
                source_file=transcript["source_file"],
                chunk_index=transcript["chunk_index"],
                content=transcript["content"]
            )
            db.add(chunk)
        
        db.commit()
        logger.info("chunks_stored_in_database")


def main():
    """Main ingestion workflow."""
    logger.info("ingestion_starting")
    
    try:
        # Step 1: Clone/update repository
        clone_or_update_repo()
        
        # Step 2: Load and chunk transcripts
        transcripts = load_transcripts()
        if not transcripts:
            logger.error("no_transcripts_found")
            return
        
        # Step 3: Generate embeddings
        embeddings = generate_embeddings(transcripts)
        
        # Step 4: Build FAISS index
        index = build_faiss_index(embeddings)
        
        # Step 5: Save index and mapping
        save_index_and_mapping(index, transcripts)
        
        # Step 6: Store chunks in database
        store_chunks_in_db(transcripts)
        
        logger.info("ingestion_completed", total_chunks=len(transcripts))
        print(f"\n✅ Ingestion complete: {len(transcripts)} chunks processed")
        
    except Exception as e:
        logger.error("ingestion_failed", error=str(e))
        raise


if __name__ == "__main__":
    main()

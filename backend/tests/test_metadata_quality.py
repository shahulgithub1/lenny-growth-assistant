"""
Tests to verify metadata quality in PostgreSQL after ingestion.
"""
import pytest
from app.db.models import TranscriptChunk
from app.db.session import SessionLocal


def get_db_session():
    """Create a database session for testing."""
    return SessionLocal()


def test_postgres_has_correct_row_count():
    """Verify PostgreSQL has approximately 10,391 chunks."""
    db = get_db_session()
    try:
        count = db.query(TranscriptChunk).count()
        assert count > 10000, f"Expected >10,000 chunks, got {count}"
        assert count < 11000, f"Expected <11,000 chunks, got {count}"
    finally:
        db.close()


def test_only_transcript_files_ingested():
    """Verify only episodes/*/transcript.md files are in database."""
    db = get_db_session()
    try:
        # Get all unique source files
        source_files = db.query(TranscriptChunk.source_file).distinct().all()
        source_files = [sf[0] for sf in source_files]
        
        # All should match pattern episodes/*/transcript.md
        for sf in source_files:
            assert sf.startswith('episodes/'), f"Source file doesn't start with 'episodes/': {sf}"
            assert sf.endswith('/transcript.md'), f"Source file doesn't end with '/transcript.md': {sf}"
            assert 'README' not in sf, f"README found in source: {sf}"
            assert 'CLAUDE' not in sf, f"CLAUDE found in source: {sf}"
    finally:
        db.close()


def test_guest_field_is_clean():
    """Verify guest field contains only the guest name, not entire frontmatter."""
    db = get_db_session()
    try:
        # Sample some chunks
        chunks = db.query(TranscriptChunk).limit(100).all()
        
        for chunk in chunks:
            # Guest should not contain these keywords from frontmatter
            assert 'title:' not in chunk.guest, f"'title:' found in guest: {chunk.guest}"
            assert 'youtube_url' not in chunk.guest, f"'youtube_url' found in guest: {chunk.guest}"
            assert 'video_id' not in chunk.guest, f"'video_id' found in guest: {chunk.guest}"
            assert 'description:' not in chunk.guest, f"'description:' found in guest: {chunk.guest}"
            assert 'keywords' not in chunk.guest, f"'keywords' found in guest: {chunk.guest}"
            
            # Guest length should be reasonable (not truncated frontmatter)
            assert len(chunk.guest) <= 255, f"Guest too long: {len(chunk.guest)} chars"
            assert len(chunk.guest) > 0, "Guest is empty"
    finally:
        db.close()


def test_episode_title_is_clean():
    """Verify episode_title is clean and meaningful."""
    db = get_db_session()
    try:
        chunks = db.query(TranscriptChunk).limit(100).all()
        
        for chunk in chunks:
            # Episode title should not be "transcript"
            assert chunk.episode_title.lower() != 'transcript', "Episode title is 'transcript'"
            
            # Should not contain YAML artifacts
            assert 'youtube_url' not in chunk.episode_title, f"'youtube_url' in title: {chunk.episode_title}"
            assert 'video_id' not in chunk.episode_title, f"'video_id' in title: {chunk.episode_title}"
            
            # Should be reasonable length
            assert len(chunk.episode_title) > 0, "Episode title is empty"
            assert len(chunk.episode_title) <= 255, f"Episode title too long: {len(chunk.episode_title)}"
    finally:
        db.close()


def test_source_file_has_meaningful_path():
    """Verify source_file contains episode path, not just 'transcript.md'."""
    db = get_db_session()
    try:
        chunks = db.query(TranscriptChunk).limit(100).all()
        
        for chunk in chunks:
            # Source file should contain episode directory
            assert '/' in chunk.source_file, f"Source file has no path: {chunk.source_file}"
            assert chunk.source_file != 'transcript.md', "Source file is just 'transcript.md'"
            assert chunk.source_file.startswith('episodes/'), f"Source doesn't start with 'episodes/': {chunk.source_file}"
    finally:
        db.close()


def test_distinct_counts():
    """Verify reasonable distinct counts."""
    db = get_db_session()
    try:
        distinct_guests = db.query(TranscriptChunk.guest).distinct().count()
        distinct_titles = db.query(TranscriptChunk.episode_title).distinct().count()
        distinct_files = db.query(TranscriptChunk.source_file).distinct().count()
        
        # Should have many distinct episodes (at least 250)
        assert distinct_guests > 250, f"Only {distinct_guests} distinct guests"
        assert distinct_titles > 250, f"Only {distinct_titles} distinct titles"
        assert distinct_files > 250, f"Only {distinct_files} distinct files"
        
        # Guests and files should be close in count
        assert abs(distinct_guests - distinct_files) < 50, \
            f"Guest count ({distinct_guests}) and file count ({distinct_files}) differ too much"
    finally:
        db.close()


def test_sample_metadata_matches_elena_verna():
    """Specific test for Elena Verna episode to verify correct parsing."""
    db = get_db_session()
    try:
        # Get a chunk from Elena Verna episode
        chunk = db.query(TranscriptChunk).filter(
            TranscriptChunk.guest == 'Elena Verna',
            TranscriptChunk.source_file == 'episodes/elena-verna/transcript.md'
        ).first()
        
        assert chunk is not None, "Elena Verna chunk not found"
        
        # Verify metadata
        assert chunk.guest == 'Elena Verna', f"Guest incorrect: {chunk.guest}"
        assert chunk.episode_title == '10 growth tactics that never work', \
            f"Title incorrect: {chunk.episode_title}"
        assert chunk.source_file == 'episodes/elena-verna/transcript.md', \
            f"Source file incorrect: {chunk.source_file}"
        
        # Verify guest field doesn't contain title
        assert 'growth tactics' not in chunk.guest, f"Title leaked into guest: {chunk.guest}"
        assert 'Amplitude' not in chunk.guest, f"Description leaked into guest: {chunk.guest}"
    finally:
        db.close()

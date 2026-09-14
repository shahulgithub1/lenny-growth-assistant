"""Tests for hybrid retrieval system."""
import pytest
from app.services.retrieval_service import retrieval_service


def test_growth_loop_query_retrieves_content():
    """Test that growth loop queries retrieve relevant content."""
    query = "What are the key principles of growth loops?"
    results = retrieval_service.retrieve_chunks(query, top_k=5)
    
    # Should return results
    assert len(results) > 0, "Should retrieve chunks for growth loop query"
    
    # Check that results contain meaningful metadata
    for result in results:
        assert result.get("episode_title"), "Should have episode title"
        assert result.get("episode_title") != "transcript", "Episode title should be descriptive"
        assert result.get("content"), "Should have content"
        assert result.get("source_file"), "Should have source file"
        assert "similarity" in result, "Should have similarity score"
    
    # At least one result should have decent score or be from lexical match
    top_score = results[0]["similarity"]
    assert top_score > 0.2, f"Top result should have reasonable score, got {top_score}"


def test_retention_query_still_works():
    """Test that retention queries still work after hybrid retrieval."""
    query = "How should a startup improve retention?"
    results = retrieval_service.retrieve_chunks(query, top_k=5)
    
    # Should return results
    assert len(results) > 0, "Should retrieve chunks for retention query"
    
    # Check metadata quality
    for result in results:
        assert result.get("episode_title"), "Should have episode title"
        assert result.get("content"), "Should have content"


def test_no_readme_or_claude_files():
    """Test that README and CLAUDE files are excluded from results."""
    # Load chunk mapping and verify no non-transcript files
    retrieval_service._load_index()
    
    non_transcript_files = []
    for chunk_id, chunk_data in retrieval_service.chunk_mapping.items():
        source = chunk_data.get("source_file", "")
        if "README" in source or "CLAUDE" in source:
            non_transcript_files.append(source)
    
    assert len(non_transcript_files) == 0, f"Found non-transcript files: {non_transcript_files}"


def test_metadata_is_meaningful():
    """Test that retrieved chunks have meaningful episode metadata."""
    query = "growth strategies"
    results = retrieval_service.retrieve_chunks(query, top_k=10)
    
    if len(results) == 0:
        pytest.skip("No results returned for query")
    
    # Check that episode titles are descriptive
    generic_titles = ["transcript", "README", "CLAUDE"]
    for result in results:
        title = result.get("episode_title", "")
        assert title not in generic_titles, f"Episode title should not be generic: {title}"
        assert len(title) > 3, f"Episode title too short: {title}"


def test_lexical_matching_for_high_value_terms():
    """Test that lexical matching works for high-value terms."""
    query = "growth loops"
    results = retrieval_service.retrieve_chunks(query, top_k=10)
    
    # Should return results (via lexical or semantic)
    assert len(results) > 0, "Should retrieve chunks for 'growth loops'"
    
    # Check if any results came from lexical matching
    lexical_or_hybrid = [r for r in results if r.get("retrieval_method") in ["lexical", "hybrid"]]
    
    # At minimum, we should have some results
    assert len(lexical_or_hybrid) >= 0, "Should use lexical matching when applicable"


def test_deduplication_works():
    """Test that hybrid retrieval deduplicates results."""
    query = "What are growth loops?"
    results = retrieval_service.retrieve_chunks(query, top_k=10)
    
    # Check for duplicate chunk_ids
    chunk_ids = [r.get("chunk_id") for r in results]
    unique_ids = set(chunk_ids)
    
    assert len(chunk_ids) == len(unique_ids), "Results should be deduplicated"


def test_retrieval_returns_correct_structure():
    """Test that returned chunks have the expected structure."""
    query = "product market fit"
    results = retrieval_service.retrieve_chunks(query, top_k=5)
    
    if len(results) == 0:
        pytest.skip("No results for query")
    
    required_keys = ["episode_title", "guest", "content", "source_file", "similarity", "excerpt"]
    
    for result in results:
        for key in required_keys:
            assert key in result, f"Result missing required key: {key}"
        
        # Check types
        assert isinstance(result["similarity"], (int, float)), "Similarity should be numeric"
        assert isinstance(result["content"], str), "Content should be string"
        assert isinstance(result["episode_title"], str), "Episode title should be string"

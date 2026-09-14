"""Tests for grounding and answer-generation behavior."""
import pytest
from app.services.agent_service import AgentService


def test_grounded_qa_prompt_requires_tool_use():
    """Test that grounded QA prompt instructs to use search tool."""
    service = AgentService(db=None)
    prompt = service._build_system_prompt("grounded_qa")
    
    assert "search_lenny_transcripts" in prompt
    assert "tool" in prompt.lower()


def test_grounded_qa_prompt_specifies_relevance_check():
    """Test that prompt distinguishes relevant vs insufficient evidence."""
    service = AgentService(db=None)
    prompt = service._build_system_prompt("grounded_qa")
    
    # Should specify when to use fallback
    assert "only" in prompt.lower() or "when" in prompt.lower()
    assert "don't have enough information" in prompt.lower() or "insufficient" in prompt.lower()
    
    # Should specify when to answer normally
    assert "relevant" in prompt.lower()
    assert "evidence" in prompt.lower() or "content" in prompt.lower()


def test_grounded_qa_prompt_forbids_contradiction():
    """Test that prompt forbids saying both 'insufficient' and answering."""
    service = AgentService(db=None)
    prompt = service._build_system_prompt("grounded_qa")
    
    # Should explicitly state fallback and answer are mutually exclusive
    assert "never" in prompt.lower() or "do not" in prompt.lower()
    assert "both" in prompt.lower() or "mutually exclusive" in prompt.lower()


def test_grounded_qa_prompt_handles_synthesis():
    """Test that prompt allows synthesis across chunks."""
    service = AgentService(db=None)
    prompt = service._build_system_prompt("grounded_qa")
    
    # Should allow combining multiple chunks
    assert "multiple" in prompt.lower() or "combine" in prompt.lower() or "synthesize" in prompt.lower()
    assert "same episode" in prompt.lower()


def test_grounded_qa_prompt_forbids_invention():
    """Test that prompt forbids inventing facts."""
    service = AgentService(db=None)
    prompt = service._build_system_prompt("grounded_qa")
    
    assert "never invent" in prompt.lower() or "do not invent" in prompt.lower()
    assert "statistics" in prompt.lower() or "facts" in prompt.lower()


def test_grounded_qa_prompt_prioritizes_requested_source():
    """Test that prompt prioritizes explicitly requested guest/episode."""
    service = AgentService(db=None)
    prompt = service._build_system_prompt("grounded_qa")
    
    # Should prioritize specific guest when requested
    assert "prioritize" in prompt.lower() or "specific" in prompt.lower()
    assert "guest" in prompt.lower() or "episode" in prompt.lower()


def test_grounded_qa_prompt_uses_conversation_context():
    """Test that prompt instructs to use conversation history."""
    service = AgentService(db=None)
    prompt = service._build_system_prompt("grounded_qa")
    
    assert "conversation" in prompt.lower() or "context" in prompt.lower() or "follow-up" in prompt.lower()
    assert "history" in prompt.lower() or "previous" in prompt.lower()


def test_grounded_qa_prompt_distinguishes_fact_vs_synthesis():
    """Test that prompt instructs to distinguish direct facts from synthesis."""
    service = AgentService(db=None)
    prompt = service._build_system_prompt("grounded_qa")
    
    assert "distinguish" in prompt.lower() or "cite" in prompt.lower()
    assert "according to" in prompt.lower() or "synthesis" in prompt.lower()


def test_routing_preserves_grounded_qa():
    """Test that general questions route to grounded_qa."""
    service = AgentService(db=None)
    
    # Product questions
    assert service._route_message("What does product-market fit look like?") == "grounded_qa"
    assert service._route_message("What are growth loops?") == "grounded_qa"
    assert service._route_message("How do I improve retention?") == "grounded_qa"
    
    # Framework questions
    assert service._route_message("According to Todd Jackson's framework, what is strong PMF?") == "grounded_qa"
    
    # Follow-up questions
    assert service._route_message("What separates developing from strong stage?") == "grounded_qa"


def test_routing_distinguishes_ship30():
    """Test that Ship 30 requests route correctly."""
    service = AgentService(db=None)
    
    assert service._route_message("Write a Ship 30 essay about retention") == "ship30"
    assert service._route_message("Create an article about growth loops") == "ship30"
    assert service._route_message("Write a blog post about PMF") == "ship30"


def test_routing_distinguishes_artifacts():
    """Test that artifact requests route correctly."""
    service = AgentService(db=None)
    
    assert service._route_message("Create a dashboard for growth metrics") == "artifact"
    assert service._route_message("Generate a framework for product-market fit") == "artifact"
    assert service._route_message("Build a template for retention analysis") == "artifact"


def test_grounded_qa_prevents_hallucination():
    """Test that grounded_qa prompt emphasizes no hallucination."""
    service = AgentService(db=None)
    prompt = service._build_system_prompt("grounded_qa")
    
    # Should emphasize using only retrieved information
    assert "only" in prompt.lower()
    assert "transcript" in prompt.lower()
    
    # Should forbid making things up
    assert "never" in prompt.lower() or "do not" in prompt.lower()
    assert "invent" in prompt.lower() or "make up" in prompt.lower()

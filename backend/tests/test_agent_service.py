"""Tests for agent service."""
import pytest
from app.services.agent_service import AgentService


def test_route_message_grounded_qa():
    """Test default routing to grounded Q&A."""
    service = AgentService(db=None)
    assert service._route_message("How to improve retention?") == "grounded_qa"
    assert service._route_message("What is product-market fit?") == "grounded_qa"


def test_route_message_ship30():
    """Test routing to Ship 30 skill."""
    service = AgentService(db=None)
    assert service._route_message("Turn this into a Ship 30 essay") == "ship30"
    assert service._route_message("Write an article about growth") == "ship30"
    assert service._route_message("Create a blog post") == "ship30"


def test_route_message_artifact():
    """Test routing to artifact skill."""
    service = AgentService(db=None)
    assert service._route_message("Create a dashboard") == "artifact"
    assert service._route_message("Generate a framework") == "artifact"
    assert service._route_message("Build a template") == "artifact"


def test_build_system_prompt_grounded_qa():
    """Test system prompt for grounded Q&A includes key instructions."""
    service = AgentService(db=None)
    prompt = service._build_system_prompt("grounded_qa")
    
    assert "research assistant" in prompt.lower()
    assert "search_lenny_transcripts" in prompt
    assert "only" in prompt.lower()  # "ONLY the information"
    assert "cite" in prompt.lower()


def test_build_system_prompt_ship30():
    """Test system prompt for Ship 30 includes writing principles."""
    service = AgentService(db=None)
    prompt = service._build_system_prompt("ship30")
    
    assert "ship 30" in prompt.lower()
    assert "hook" in prompt.lower()
    assert "narrative" in prompt.lower()
    assert "bold" in prompt.lower()
    assert "1,250" in prompt or "1250" in prompt


def test_build_system_prompt_artifact():
    """Test system prompt for artifacts includes safety and quality constraints."""
    service = AgentService(db=None)
    prompt = service._build_system_prompt("artifact")
    
    assert "html" in prompt.lower()
    assert "markdown" in prompt.lower()
    # Check for self-contained requirements
    assert "css must be in a <style> tag" in prompt.lower()
    assert "javascript must be in a <script> tag" in prompt.lower()
    # Check for security constraints
    assert "no external" in prompt.lower() or "no separate" in prompt.lower()
    assert "no eval()" in prompt.lower()
    # Check for quality requirements
    assert "polished" in prompt.lower() or "professional" in prompt.lower()

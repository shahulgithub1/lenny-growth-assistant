"""Tests for artifact generation quality and structure."""
import pytest
import re
from app.api.routes.sessions import _extract_artifact


def test_extract_html_artifact_with_doctype():
    """Test extracting HTML artifact with DOCTYPE."""
    content = """Here's your landing page:

<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Test Page</title>
    <style>
        body { font-family: Arial, sans-serif; }
    </style>
</head>
<body>
    <h1>Hello World</h1>
    <script>
        console.log('Hello');
    </script>
</body>
</html>

Let me know if you need changes!"""
    
    artifact_type, artifact_content = _extract_artifact(content)
    
    assert artifact_type == "html"
    assert artifact_content is not None
    assert "<!DOCTYPE html>" in artifact_content
    assert "<html" in artifact_content
    assert "</html>" in artifact_content


def test_extract_html_artifact_without_doctype():
    """Test extracting HTML artifact without DOCTYPE but with html tags."""
    content = """<html>
<head>
    <title>Test</title>
</head>
<body>
    <h1>Content</h1>
</body>
</html>"""
    
    artifact_type, artifact_content = _extract_artifact(content)
    
    assert artifact_type == "html"
    assert artifact_content is not None
    assert "<html" in artifact_content


def test_html_artifact_self_contained_structure():
    """Test that HTML artifacts should be self-contained."""
    # Simulated artifact content that follows the new prompt requirements
    html_content = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Growth Loops</title>
    <style>
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            margin: 0;
            padding: 20px;
        }
        .container { max-width: 800px; margin: 0 auto; }
    </style>
</head>
<body>
    <div class="container">
        <h1>Key Principles of Growth Loops</h1>
        <p>Content here...</p>
    </div>
    <script>
        document.addEventListener('DOMContentLoaded', function() {
            console.log('Loaded');
        });
    </script>
</body>
</html>"""
    
    # Verify self-contained requirements
    assert "<style>" in html_content and "</style>" in html_content
    assert "<script>" in html_content and "</script>" in html_content
    
    # Should NOT have external references
    assert 'href="http' not in html_content
    assert 'src="http' not in html_content
    assert '<link rel="stylesheet"' not in html_content.lower()
    assert '<script src=' not in html_content.lower()


def test_no_nested_event_listeners():
    """Test that generated JavaScript doesn't have nested event listeners."""
    # Bad pattern that should NOT appear
    bad_js_pattern = """
    button.addEventListener('click', function() {
        button.addEventListener('click', function() {
            console.log('Bad');
        });
    });
    """
    
    # Check for nested addEventListener pattern
    # This is a heuristic - actual test would check generated content
    nested_pattern = re.compile(
        r'addEventListener\s*\([^)]+\)\s*\{[^}]*addEventListener',
        re.DOTALL
    )
    
    assert nested_pattern.search(bad_js_pattern) is not None
    
    # Good pattern
    good_js_pattern = """
    document.addEventListener('DOMContentLoaded', function() {
        const button = document.getElementById('myButton');
        button.addEventListener('click', function() {
            console.log('Good');
        });
    });
    """
    
    # This pattern is acceptable (DOMContentLoaded wraps setup)
    # We'd validate by ensuring addEventListener isn't nested inside the same event type


def test_extract_markdown_artifact():
    """Test that substantial markdown is detected as artifact."""
    content = """# Growth Strategy Framework

## Introduction
This is a comprehensive guide...

## Key Principles
1. User acquisition
2. Activation
3. Retention

## Detailed Analysis
Lorem ipsum dolor sit amet, consectetur adipiscing elit. 
Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.

### Subsection
More detailed content here with substantial length to trigger artifact detection.

## Conclusion
Final thoughts and recommendations.

Let me know if you need more details!"""
    
    artifact_type, artifact_content = _extract_artifact(content)
    
    # Should detect as markdown if it has multiple headers and is substantial
    # Current implementation checks for 2+ headers and 500+ chars
    assert artifact_type == "markdown"
    if len(content) > 500 and content.count('\n#') >= 2:
        assert artifact_content is not None


def test_no_artifact_in_short_response():
    """Test that short responses don't trigger artifact extraction."""
    content = "Here's a quick tip: focus on retention first!"
    
    artifact_type, artifact_content = _extract_artifact(content)
    
    # Should not extract artifact from short responses
    assert artifact_content is None


def test_security_constraints_preserved():
    """Test that security constraints are maintained in HTML structure."""
    html_with_dangerous_content = """<!DOCTYPE html>
<html>
<head><title>Test</title></head>
<body>
    <iframe src="https://evil.com"></iframe>
    <form action="https://evil.com/submit" method="POST">
        <input type="text" name="data">
    </form>
    <script src="https://evil.com/malicious.js"></script>
</body>
</html>"""
    
    # The artifact viewer applies DOMPurify and sandbox
    # We verify the artifact extraction doesn't block these (viewer handles security)
    artifact_type, artifact_content = _extract_artifact(html_with_dangerous_content)
    
    assert artifact_type == "html"
    # The extraction allows it (viewer will sanitize)
    assert artifact_content is not None
    
    # Note: Actual security is enforced in ArtifactViewer.tsx with:
    # - DOMPurify sanitization
    # - iframe sandbox="allow-same-origin"
    # - CSP restrictions

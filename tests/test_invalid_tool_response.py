import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.tools.summarize_text.summarize_text import SummarizeTextTool
import pytest

def test_invalid_mcp_response(monkeypatch):
    """Test that the summarize_text tool raises ValueError for invalid output data."""
    tool = SummarizeTextTool()

    def broken_summarize(text: str) -> dict:
        return {
            "json": {"unexpected": "format"} 
        }

    monkeypatch.setattr(
        tool.service, "summarize", broken_summarize
    )

    with pytest.raises(ValueError, match="Invalid output data:"):
        tool.run("Test content")
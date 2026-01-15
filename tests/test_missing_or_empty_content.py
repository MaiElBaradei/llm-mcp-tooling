import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from tests.mcp_client import SummarizationMCPClient
import pytest

@pytest.mark.asyncio
async def test_empty_extracted_content():
    mcp_client = SummarizationMCPClient()
    await mcp_client.connect()

    empty_text = ""

    response = await mcp_client.summarize_text(empty_text)
    print(response)

    assert "empty" in response[0]["text"].lower()
    await mcp_client.close()
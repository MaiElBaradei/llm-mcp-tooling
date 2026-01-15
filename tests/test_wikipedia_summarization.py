import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pytest
import asyncio
from playwright.async_api import async_playwright
from tests.mcp_client import SummarizationMCPClient
import json

WIKI_URL = "https://en.wikipedia.org/wiki/Main_Page"
SEARCH_TERM = "Artificial intelligence"

@pytest.mark.asyncio
async def test_wikipedia_ai_history_summarization():
    # 1️⃣ Start MCP Client
    mcp_client = SummarizationMCPClient()
    await mcp_client.connect()

    # 2️⃣ Start Playwright (Firefox)
    async with async_playwright() as p:
        browser = await p.firefox.launch(headless=True)
        context = await browser.new_context()
        page = await context.new_page()

        # 3️⃣ Navigate to Wikipedia home
        await page.goto(WIKI_URL, timeout=30_000)

        # 4️⃣ Locate search input
        search_input = page.locator("input[id='searchInput']")
        await search_input.wait_for(state="visible")

        # 5️⃣ Enter term and submit
        await search_input.fill(SEARCH_TERM)
        await search_input.press("Enter")

        # 6️⃣ Click first search result (page title)
        first_heading = page.locator("h1#firstHeading")
        await first_heading.wait_for()
        assert SEARCH_TERM.lower() in (await first_heading.text_content()).lower()

        # 7️⃣ Scroll to specific section heading
        history_heading = page.locator(f"h2#History")
        await history_heading.scroll_into_view_if_needed()
        await history_heading.wait_for()

        # 8️⃣ Extract paragraph text under heading
        # From the h2, go up to parent div, then get following p siblings
        paragraphs = history_heading.locator("xpath=../following-sibling::p")

        extracted_text = ""
        count = await paragraphs.count()

        for i in range(min(count, 3)):  # limit for test stability
            extracted_text += (await paragraphs.nth(i).text_content()) + "\n"

        # ✅ Assertion: Text extraction
        assert len(extracted_text.strip()) > 300
        assert "intelligence" in extracted_text.lower()

        # 9️⃣ Send extracted text to MCP summarization tool
        result = await mcp_client.summarize_text(extracted_text)

        # 🔟 Structured Assertions on MCP output
        assert result is not None
        assert len(result) > 0
        result_dict = result[0]
        assert isinstance(result_dict, dict)

        assert "text" in result_dict
        assert isinstance(result_dict["text"], str)
        result_text = dict(json.loads(result_dict["text"]))

        assert "summary" in result_text
        assert isinstance(result_text["summary"], str)
        assert len(result_text["summary"]) > 50
    
        assert "metadata" in result_text
        assert "prompt" in result_text
        # Cleanup
        await browser.close()
        await mcp_client.close()

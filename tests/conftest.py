import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pytest
import asyncio
from typing import AsyncGenerator
from playwright.async_api import async_playwright, Browser, Page

from tests.mcp_client import SummarizationMCPClient

@pytest.fixture(scope="session")
def event_loop():
    """
    Create an event loop for the entire test session.
    Prevents 'Event loop is closed' errors.
    """
    loop = asyncio.new_event_loop()
    yield loop
    loop.close()

@pytest.fixture(scope="session")
async def browser() -> AsyncGenerator[Browser, None]:
    async with async_playwright() as p:
        browser = await p.firefox.launch(headless=True)
        yield browser
        await browser.close()

@pytest.fixture(scope="session")
async def browser() -> AsyncGenerator[Browser, None]:
    async with async_playwright() as p:
        browser = await p.firefox.launch(headless=True)
        yield browser
        await browser.close()

@pytest.fixture
async def page(browser: Browser) -> AsyncGenerator[Page, None]:
    context = await browser.new_context()
    page = await context.new_page()
    yield page
    await context.close()




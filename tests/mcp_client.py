import os
from typing import Any, Dict
from mcp import ClientSession
from mcp.client.sse import sse_client
from langchain_mcp_adapters.tools import load_mcp_tools
from contextlib import AsyncExitStack


class SummarizationMCPClient:
    def __init__(self, server_url: str = None):
        if server_url is None:
            server_url = os.getenv(
                "SUMMARIZATION_SERVER_URL",
                "http://127.0.0.1:8001/sse"
            )
        
        self.server_url = server_url
        self.session = None
        self.stack = AsyncExitStack()
        self.tools = {}

    async def connect(self):
        try:
            read, write = await self.stack.enter_async_context(
                sse_client(self.server_url)
            )
            
            self.session = await self.stack.enter_async_context(
                ClientSession(read, write)
            )

            await self.session.initialize()

            tools = await load_mcp_tools(self.session)
            self.tools = {t.name: t for t in tools}
            
        except Exception as e:
            raise

    async def summarize_text(self, text: str) -> Dict[str, Any]:
        if "summarize_text" not in self.tools:
            raise ValueError("summarize_text tool not available")
        
        tool = self.tools["summarize_text"]
        return await tool.ainvoke({"text": text})

    async def close(self):
        await self.stack.aclose()

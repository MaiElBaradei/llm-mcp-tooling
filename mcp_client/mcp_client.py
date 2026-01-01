from google import genai
from google.genai import types
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
import os
from dotenv import load_dotenv
load_dotenv()


client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

#!/usr/bin/env python
"""
MCP Client with Multiple Servers using LangChain MCP Adapters, LangGraph, and Gemini API

This client:
- Loads MCP server configuration from a JSON file
- Connects to multiple MCP servers
- Loads tools from all servers using LangChain MCP adapters
- Creates a unified LangGraph React agent with Gemini
- Runs an interactive chat loop with tool visibility
"""

import asyncio
import os
import sys
import json
from contextlib import AsyncExitStack
from typing import Dict, List

# MCP Client Imports
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

# LangChain & LangGraph Imports
from langchain_mcp_adapters.tools import load_mcp_tools
from langgraph.prebuilt import create_react_agent
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import AIMessage, HumanMessage

# Environment Setup
from dotenv import load_dotenv
load_dotenv()


# ---------------------------
# Custom JSON Encoder for LangChain objects
# ---------------------------
class CustomEncoder(json.JSONEncoder):
    """
    Custom JSON encoder to handle non-serializable objects returned by LangChain.
    """
    def default(self, o):
        if hasattr(o, "content"):
            return {"type": o.__class__.__name__, "content": o.content}
        return super().default(o)


# ---------------------------
# Function: read_config_json
# ---------------------------
def read_config_json():
    """
    Reads the MCP server configuration JSON.
    Priority:
      1. Try MCP_SERVER_CONFIG environment variable
      2. Fallback to default 'mcp_server_config.json' in same directory
    
    Returns:
        dict: Parsed JSON content with MCP server definitions
    """
    config_path = os.getenv("MCP_SERVER_CONFIG")
    if not config_path:
        script_dir = os.path.dirname(os.path.abspath(__file__))
        config_path = os.path.join(script_dir, "servers_config.json")
        print(f"MCP_SERVER_CONFIG not set. Falling back to: {config_path}")
    
    try:
        with open(config_path, "r") as f:
            return json.load(f)
    except Exception as e:
        print(f"Failed to read config file at '{config_path}': {e}")
        sys.exit(1)


# ---------------------------
# Google Gemini LLM Instantiation
# ---------------------------
llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    temperature=0,
    max_retries=2,
    google_api_key=os.getenv("GEMINI_API_KEY")
)


# ---------------------------
# Main Function: run_agent
# ---------------------------
async def run_agent():
    """
    Connects to all MCP servers defined in the configuration,
    loads their tools, creates a unified React agent,
    and starts an interactive loop.
    """
    config = read_config_json()
    mcp_servers = config.get("mcpServers", {})
    
    if not mcp_servers:
        print("No MCP servers found in the configuration.")
        return
    
    tools = []
    
    # Use AsyncExitStack to manage multiple async resources
    async with AsyncExitStack() as stack:
        # Connect to each MCP server
        for server_name, server_info in mcp_servers.items():
            print(f"\n🔌 Connecting to MCP Server: {server_name}...")
            
            server_params = StdioServerParameters(
                command=server_info["command"],
                args=server_info["args"]
            )
            
            try:
                # Establish stdio connection to the server
                read, write = await stack.enter_async_context(
                    stdio_client(server_params)
                )
                
                # Create client session
                session = await stack.enter_async_context(
                    ClientSession(read, write)
                )
                
                # Initialize the session
                await session.initialize()
                
                # Load MCP tools using LangChain adapter
                server_tools = await load_mcp_tools(session)
                
                # Add tools to aggregated list
                for tool in server_tools:
                    print(f"  🔧 Loaded tool: {tool.name}")
                    tools.append(tool)
                
                print(f"  ✅ {len(server_tools)} tools loaded from {server_name}")
                
            except Exception as e:
                print(f"  ❌ Failed to connect to server {server_name}: {e}")
        
        # Check if any tools were loaded
        if not tools:
            print("\n❌ No tools loaded from any server. Exiting.")
            return
        
        print(f"\n✅ Total tools loaded: {len(tools)}")
        
        # Create React agent with Gemini and all tools
        print("\n🤖 Creating LangGraph React Agent with Gemini...")
        agent = create_react_agent(llm, tools)
        
        # Start interactive chat loop
        print("\n" + "="*60)
        print("🚀 MCP Client Ready!")
        print("="*60)
        print("\nAvailable commands:")
        print("  - Type your query to interact with the agent")
        print("  - Type 'tools' to list all available tools")
        print("  - Type 'quit' to exit")
        print("="*60)
        
        # Initialize chat history
        chat_history = []
        
        while True:
            query = input("\n💬 Query: ").strip()
            
            if query.lower() == "quit":
                print("\n👋 Goodbye!")
                break
            
            if query.lower() == "tools":
                print("\n📋 Available Tools:")
                for i, tool in enumerate(tools, 1):
                    print(f"  {i}. {tool.name}")
                    if hasattr(tool, 'description'):
                        print(f"     Description: {tool.description}")
                continue
            
            if not query:
                continue
            
            # Add user message to chat history
            chat_history.append(HumanMessage(content=query))
            
            try:
                print("\n🤔 Thinking...")
                
                # Invoke agent with full chat history
                response = await agent.ainvoke({"messages": chat_history})
                
                # Extract AI message content
                ai_message_content = None
                
                if isinstance(response, dict) and "content" in response:
                    ai_message_content = response["content"]
                elif isinstance(response, dict) and "messages" in response:
                    # Find last AIMessage
                    for msg in reversed(response["messages"]):
                        if msg.__class__.__name__ == "AIMessage":
                            ai_message_content = msg.content
                            break
                    if not ai_message_content:
                        ai_message_content = str(response)
                else:
                    ai_message_content = str(response)
                
                # Add AIMessage to chat history
                chat_history.append(AIMessage(content=ai_message_content))
                
                # Print response
                print("\n🤖 Response:")
                print("-" * 60)
                try:
                    formatted = json.dumps(
                        {"type": "AIMessage", "content": ai_message_content},
                        indent=2,
                        cls=CustomEncoder
                    )
                    print(formatted)
                except Exception:
                    print(ai_message_content)
                print("-" * 60)
                
            except Exception as e:
                print(f"\n❌ Error: {e}")
                import traceback
                traceback.print_exc()


# ---------------------------
# Entry Point
# ---------------------------
if __name__ == "__main__":
    asyncio.run(run_agent())
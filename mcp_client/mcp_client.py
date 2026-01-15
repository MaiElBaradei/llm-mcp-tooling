#!/usr/bin/env python
"""
MCP Client with Multiple Servers using LangChain MCP Adapters, LangGraph, and Gemini API

This client:
- Loads MCP server configuration from a JSON file
- Connects to multiple MCP servers
- Loads tools from all servers using LangChain MCP adapters
- Creates a unified LangGraph React agent with Gemini
- Supports both LLM-powered and manual tool calls
- Runs an interactive chat loop with tool visibility
"""

import asyncio
import os
import sys
import json
from contextlib import AsyncExitStack
from typing import Dict, List, Any
import traceback

# MCP Client Imports
from mcp import ClientSession
from mcp.client.sse import sse_client

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
      2. Fallback to default 'servers_config.json' in same directory
    
    Returns:
        dict: Parsed JSON content with MCP server definitions
    """

    script_dir = os.path.dirname(os.path.abspath(__file__))
    config_path = os.path.join(script_dir, "servers_config.json")
    
    try:
        with open(config_path, "r") as f:
            return json.load(f)
    except Exception as e:
        print(f"Failed to read config file at '{config_path}': {e}")
        sys.exit(1)


# ---------------------------
# Google Gemini LLM Instantiation
# ---------------------------
if not os.getenv("GOOGLE_API_KEY"):
    raise ValueError("GOOGLE_API_KEY not found")
llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    temperature=0,
    max_retries=2,
    google_api_key=os.getenv("GOOGLE_API_KEY")
)


# ---------------------------
# MCPClient Class for Session Management
# ---------------------------
class MCPClientManager:
    """Manages MCP server connections and tool access."""
    
    def __init__(self):
        self.sessions: Dict[str, ClientSession] = {}
        self.tools_by_name: Dict[str, Any] = {}
        self.server_by_tool: Dict[str, str] = {}
        self.agent = None
        self.stack: AsyncExitStack = None
    
    async def initialize(self, config: Dict) -> List[Any]:
        """Initialize all MCP servers and load tools.
        
        Args:
            config: Configuration dictionary
            
        Returns:
            List of loaded tools
        """
        mcp_servers = config.get("mcpServers", {})
        
        if not mcp_servers:
            print("No MCP servers found in the configuration.")
            return []
        
        tools = []
        self.stack = AsyncExitStack()
        
        # Connect to each MCP server
        for server_name, server_info in mcp_servers.items():
            print(f"\n🔌 Connecting to MCP Server: {server_name}...")
            
            url = server_info.get("url")
            if not url:
                print(f"  ❌ Server '{server_name}' has no 'url' defined in config")
                continue
            
            print(f"  📍 URL: {url}")
            
            try:
                # Establish SSE connection - sse_client creates its own HTTP client
                print(f"  🔗 Establishing SSE connection...")
                read, write = await self.stack.enter_async_context(
                    sse_client(url)
                )
                
                # Create client session
                print(f"  📡 Creating client session...")
                session = await self.stack.enter_async_context(
                    ClientSession(read, write)
                )
                
                # Initialize the session
                print(f"  🚀 Initializing session...")
                await session.initialize()
                self.sessions[server_name] = session
                
                # Load MCP tools using LangChain adapter
                print(f"  🔧 Loading tools...")
                server_tools = await load_mcp_tools(session)
                
                # Add tools to aggregated list and create mapping
                for tool in server_tools:
                    print(f"  🔧 Loaded tool: {tool.name}")
                    tools.append(tool)
                    self.tools_by_name[tool.name] = tool
                    self.server_by_tool[tool.name] = server_name
                
                print(f"  ✅ {len(server_tools)} tools loaded from {server_name}")
                
            except Exception as e:
                print(f"  ❌ Failed to connect to server {server_name}")
                print(f"     Error: {e}")
                print(f"     Full traceback:")
                traceback.print_exc()
        
        if not tools:
            print("\n❌ No tools loaded from any server.")
            await self.cleanup()
            return []
        
        print(f"\n✅ Total tools loaded: {len(tools)}")
        
        # Create React agent with Gemini and all tools
        print("\n🤖 Creating LangGraph React Agent with Gemini...")
        self.agent = create_react_agent(llm, tools)
        
        return tools
    
    async def cleanup(self):
        """Clean up resources."""
        if self.stack:
            try:
                await self.stack.aclose()
            except Exception as e:
                # Silently ignore cleanup errors
                pass
    
    async def call_tool_manually(self, tool_name: str, args: Dict[str, Any]) -> str:
        """Call a tool directly without going through the agent.
        
        Args:
            tool_name: Name of the tool to call
            args: Arguments for the tool
            
        Returns:
            Tool result as string
        """
        if tool_name not in self.tools_by_name:
            return f"❌ Error: Tool '{tool_name}' not found"
        
        tool = self.tools_by_name[tool_name]
        server_name = self.server_by_tool[tool_name]
        
        print(f"\n🔨 Calling tool '{tool_name}' on server '{server_name}'")
        print(f"   Arguments: {json.dumps(args, indent=2)}")
        
        try:
            # Invoke the tool directly
            result = await tool.ainvoke(args)
            print(f"   ✅ Tool execution successful")
            return str(result)
        except Exception as e:
            print(f"   ❌ Tool execution failed: {str(e)}")
            return f"Error calling tool: {str(e)}"


# ---------------------------
# Helper Functions for Manual Tool Calling
# ---------------------------
def get_tool_arguments_interactively(tool: Any) -> Dict[str, Any]:
    """
    Get tool arguments by asking user for each parameter individually.
    
    Args:
        tool: The tool object with args_schema
        
    Returns:
        Dictionary of argument names and values
    """
    args = {}
    
    # Try to get parameters from args_schema
    if not hasattr(tool, 'args_schema') or not tool.args_schema:
        print("⚠️  No parameter schema found for this tool")
        args_input = input("Enter arguments as JSON (or press Enter for none): ").strip()
        try:
            return json.loads(args_input) if args_input else {}
        except json.JSONDecodeError:
            print("❌ Invalid JSON format")
            return {}
    
    # Get the schema
    schema = tool.args_schema
    
    # Handle different schema types
    if hasattr(schema, 'model_fields'):
        # Pydantic model
        properties = schema.model_fields
        print("\n📝 Tool Parameters:")
        print("-" * 70)
        
        for param_name, field_info in properties.items():
            # Get description and type info
            description = field_info.description or "No description"
            field_type = field_info.annotation if hasattr(field_info, 'annotation') else "string"
            
            # Format type name
            type_name = str(field_type).split("'")[1] if "'" in str(field_type) else str(field_type)
            
            print(f"\n🔹 {param_name}")
            print(f"   Type: {type_name}")
            print(f"   Description: {description}")
            
            # Check if required
            is_required = field_info.is_required() if hasattr(field_info, 'is_required') else True
            required_str = "(Required)" if is_required else "(Optional)"
            
            # Get user input
            while True:
                value = input(f"   Enter value {required_str}: ").strip()
                
                if not value:
                    if is_required:
                        print(f"   ❌ This parameter is required")
                        continue
                    else:
                        break
                
                # Try to convert to appropriate type
                try:
                    if field_type == int or type_name == "int":
                        args[param_name] = int(value)
                    elif field_type == float or type_name == "float":
                        args[param_name] = float(value)
                    elif field_type == bool or type_name == "bool":
                        args[param_name] = value.lower() in ("true", "yes", "1")
                    else:
                        args[param_name] = value
                    break
                except ValueError:
                    print(f"   ❌ Cannot convert '{value}' to {type_name}. Try again.")
        
        print("\n" + "-" * 70)
    
    elif isinstance(schema, dict) and 'properties' in schema:
        # JSON schema format
        properties = schema.get('properties', {})
        required_fields = schema.get('required', [])
        
        print("\n📝 Tool Parameters:")
        print("-" * 70)
        
        for param_name, param_schema in properties.items():
            param_type = param_schema.get('type', 'string')
            is_required = param_name in required_fields
            
            print(f"\n🔹 {param_name}")
            print(f"   Type: {param_type}")
            
            required_str = "(Required)" if is_required else "(Optional)"
            
            # Get user input
            while True:
                value = input(f"   Enter value {required_str}: ").strip()
                
                if not value:
                    if is_required:
                        print(f"   ❌ This parameter is required")
                        continue
                    else:
                        break
                
                # Try to convert to appropriate type
                try:
                    if param_type == "integer":
                        args[param_name] = int(value)
                    elif param_type == "number":
                        args[param_name] = float(value)
                    elif param_type == "boolean":
                        args[param_name] = value.lower() in ("true", "yes", "1")
                    else:
                        args[param_name] = value
                    break
                except ValueError:
                    print(f"   ❌ Cannot convert '{value}' to {param_type}. Try again.")
        
        print("\n" + "-" * 70)
    
    else:
        # Fallback to JSON input
        print("⚠️  Using JSON input format")
        args_input = input("Enter arguments as JSON: ").strip()
        try:
            args = json.loads(args_input) if args_input else {}
        except json.JSONDecodeError:
            print("❌ Invalid JSON format")
            args = {}
    
    return args


# ---------------------------
# Interactive Commands Handler
# ---------------------------
def print_help():
    """Print help information."""
    print("\n" + "="*70)
    print("📚 Available Commands:")
    print("="*70)
    print("\n  LLM-Powered Queries:")
    print("    • Type any question or request to use Gemini agent")
    print("    • Example: 'Summarize this PDF: /path/to/file.pdf'")
    print("\n  Manual Tool Calls:")
    print("    • manual              - Manually call a specific tool")
    print("    • manual-list         - Show tool names and parameters")
    print("\n  Information:")
    print("    • tools               - List all available tools")
    print("    • help                - Show this help message")
    print("\n  Control:")
    print("    • quit                - Exit the client")
    print("="*70 + "\n")


async def interactive_mode(manager: MCPClientManager):
    """Run interactive chat loop with manual and LLM tool calling.
    
    Args:
        manager: MCPClientManager instance
    """
    print("\n" + "="*70)
    print("🚀 MCP Client Ready!")
    print("="*70)
    print("\n📖 USAGE INSTRUCTIONS")
    print("-"*70)
    print("\n1️⃣  LLM-POWERED TOOL CALLING (Recommended)")
    print("   Gemini AI automatically selects and calls the right tools")
    print("   ")
    print("   Examples:")
    print("   • 'Summarize the PDF at /path/to/document.pdf'")
    print("   • 'What is the weather in London?'")
    print("   • 'Convert 100 USD to EUR'")
    print("   • 'Detect the language of this text: Bonjour'")
    print("\n2️⃣  MANUAL TOOL CALLING (Direct Control)")
    print("   Call specific tools with exact parameters")
    print("   ")
    print("   Commands:")
    print("   • 'manual'             - Interactively select and call a tool")
    print("   • 'manual-list'        - Show all tools and their parameters")
    print("\n3️⃣  OTHER COMMANDS")
    print("   • 'tools'              - List all available tools")
    print("   • 'help'               - Show all commands")
    print("   • 'quit'               - Exit the program")
    print("\n" + "="*70)
    print("💡 TIP: Start with LLM queries for natural language interactions")
    print("        Use manual calls for precise tool control")
    print("="*70)
    
    chat_history = []
    
    while True:
        try:
            query = input("\n💬 Query: ").strip()
            
            if not query:
                continue
            
            # Handle special commands
            if query.lower() == "quit":
                print("\n👋 Goodbye!")
                break
            
            elif query.lower() == "help":
                print_help()
            
            elif query.lower() == "tools":
                print("\n📋 Available Tools:")
                for i, tool_name in enumerate(sorted(manager.tools_by_name.keys()), 1):
                    tool = manager.tools_by_name[tool_name]
                    server = manager.server_by_tool[tool_name]
                    print(f"  {i}. {tool_name} (from '{server}')")
                    if hasattr(tool, 'description'):
                        print(f"     📝 {tool.description}")
                continue
            
            elif query.lower() == "manual-list":
                print("\n📋 Tool Details for Manual Calls:")
                for tool_name in sorted(manager.tools_by_name.keys()):
                    tool = manager.tools_by_name[tool_name]
                    server = manager.server_by_tool[tool_name]
                    print(f"\n  🔧 {tool_name}")
                    print(f"     Server: {server}")
                    if hasattr(tool, 'description'):
                        print(f"     Description: {tool.description}")
                    if hasattr(tool, 'args_schema') and tool.args_schema:
                        print(f"     Parameters: {tool.args_schema}")
                continue
            
            elif query.lower() == "manual":
                # Manual tool call flow
                print("\n" + "-"*70)
                print("🔨 Manual Tool Call")
                print("-"*70)
                
                # List tools
                tool_list = sorted(manager.tools_by_name.keys())
                print("\nAvailable tools:")
                for i, name in enumerate(tool_list, 1):
                    print(f"  {i}. {name}")
                
                try:
                    tool_choice = input("\nSelect tool (number or name): ").strip()
                    
                    # Handle numeric selection
                    if tool_choice.isdigit():
                        tool_idx = int(tool_choice) - 1
                        if 0 <= tool_idx < len(tool_list):
                            tool_name = tool_list[tool_idx]
                        else:
                            print("❌ Invalid selection")
                            continue
                    else:
                        tool_name = tool_choice
                    
                    if tool_name not in manager.tools_by_name:
                        print(f"❌ Tool '{tool_name}' not found")
                        continue
                    
                    # Get tool and show its details
                    tool = manager.tools_by_name[tool_name]
                    print(f"\n✅ Selected tool: {tool_name}")
                    if hasattr(tool, 'description'):
                        print(f"📝 Description: {tool.description}")
                    
                    # Get arguments interactively from user
                    args = get_tool_arguments_interactively(tool)
                    
                    # Call tool
                    result = await manager.call_tool_manually(tool_name, args)
                    print("\n📤 Result:")
                    print("-"*70)
                    print(result)
                    print("-"*70)
                    
                except KeyboardInterrupt:
                    print("\n⚠️ Cancelled")
                    continue
            
            else:
                # Process as LLM query
                chat_history.append(HumanMessage(content=query))
                
                try:
                    print("\n🤔 Thinking...")
                    
                    # Invoke agent with full chat history
                    response = await manager.agent.ainvoke({"messages": chat_history})
                    
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
                    print("-" * 70)
                    try:
                        formatted = json.dumps(
                            {"type": "AIMessage", "content": ai_message_content},
                            indent=2,
                            cls=CustomEncoder
                        )
                        print(formatted)
                    except Exception:
                        print(ai_message_content)
                    print("-" * 70)
                    
                except Exception as e:
                    print(f"\n❌ Error: {e}")
                    import traceback
                    traceback.print_exc()
        
        except KeyboardInterrupt:
            print("\n\n👋 Interrupted by user")
            break
        except Exception as e:
            print(f"\n❌ Unexpected error: {e}")
            import traceback
            traceback.print_exc()


# ---------------------------
# Main Function
# ---------------------------
async def main():
    """Main entry point."""
    config = read_config_json()
    
    manager = MCPClientManager()
    tools = await manager.initialize(config)
    
    if not tools:
        await manager.cleanup()
        return
    
    try:
        await interactive_mode(manager)
    finally:
        # Ensure proper cleanup on exit
        await manager.cleanup()
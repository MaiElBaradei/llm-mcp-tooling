# MCP Servers

This directory contains three Model Context Protocol (MCP) servers that expose the tools from the AI QA assignment.

## MCP Servers

### 1. Summarization Server (`summarization_server.py`)

Exposes text and document processing tools:
- **extract_pdf_text** - Extract text from PDF files (local or URL)
- **summarize_text** - Summarize text using an LLM
- **summarize_pdf** - Summarize PDF documents
- **detect_language** - Detect the language of text

### 2. External API Tooling Server (`external_api_server.py`)

Exposes external API integration tools:
- **fetch_weather** - Get current weather for a city
- **fetch_exchange_rate** - Get exchange rates for currency pairs

### 3. Evaluation Server (`evaluation_server.py`)

Exposes LLM evaluation and quality assurance tools:
- **evaluate_llm_responses** - Evaluate LLM responses against ground truth
- **hallucination_checker** - Check for hallucinations in LLM responses

## Setup Instructions

### Prerequisites

- Python 3.10 or higher
- MCP SDK installed: `pip install "mcp[cli]"`
- Project dependencies installed

### Installation

1. Install MCP dependencies:
```bash
pip install "mcp[cli]" httpx
```

2. Ensure your project's app package is in the Python path

### Running the Servers

Each server can be run individually:

```bash
# Terminal 1: Start Summarization Server
python mcp_servers/summarization_server.py

# Terminal 2: Start External API Server
python mcp_servers/external_api_server.py

# Terminal 3: Start Evaluation Server
python mcp_servers/evaluation_server.py
```

### Connecting to Claude for Desktop

To use these servers with Claude for Desktop, configure them in `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "summarization": {
      "command": "python",
      "args": [
        "/absolute/path/to/mcp_servers/summarization_server.py"
      ]
    },
    "external-api": {
      "command": "python",
      "args": [
        "/absolute/path/to/mcp_servers/external_api_server.py"
      ]
    },
    "evaluation": {
      "command": "python",
      "args": [
        "/absolute/path/to/mcp_servers/evaluation_server.py"
      ]
    }
  }
}
```

On Windows, the config file is located at:
```
%AppData%\Claude\claude_desktop_config.json
```

On macOS:
```
~/Library/Application Support/Claude/claude_desktop_config.json
```

On Linux:
```
~/.config/Claude/claude_desktop_config.json
```

### Important Notes

⚠️ **STDIO Communication**: These servers use STDIO transport which means:
- Do NOT use `print()` statements (use logging instead)
- All logging is configured to write to stderr
- stdout is reserved for JSON-RPC message communication

✅ **Logging**: All servers are configured to log to stderr using Python's logging module.

### Architecture

All servers follow the FastMCP pattern:
1. Use the `@mcp.tool()` decorator to define tools
2. Leverage type hints for automatic tool schema generation
3. Wrap existing tool implementations
4. Convert return values to strings for consistency
5. Include proper error handling

### Testing

To test a server locally:

```bash
# Start the server
python mcp_servers/summarization_server.py

# In another terminal, test with MCP CLI
mcp request <server_name> <tool_name> --arguments '{"arg": "value"}'
```

## Tool Details

### Summarization Server Tools

**extract_pdf_text**
- Input: `pdf_path_or_url` (string) - Path or URL to PDF
- Output: Extracted text and page count

**summarize_text**
- Input: `text` (string) - Text to summarize
- Output: Summary with metadata

**summarize_pdf**
- Input: `file_path` (string) - Path or URL to PDF
- Output: PDF summary

**detect_language**
- Input: `text` (string) - Text to analyze
- Output: Language code and confidence score

### External API Server Tools

**fetch_weather**
- Input: `city` (string) - City name
- Output: Temperature, wind speed, condition, metadata

**fetch_exchange_rate**
- Input: `base_currency` (string), `target_currency` (string) - Currency codes
- Output: Exchange rate with provider and timestamp

### Evaluation Server Tools

**evaluate_llm_responses**
- Input: `ground_truth` (string), `response` (string)
- Output: Similarity scores (cosine, lexical, conciseness)

**hallucination_checker**
- Input: `ground_truth` (string), `response` (string)
- Output: Hallucination detection results with explanation

## Troubleshooting

### Server doesn't appear in Claude for Desktop
1. Restart Claude for Desktop after updating config
2. Check the absolute path is correct (use `pwd` on Linux/macOS or `cd` on Windows)
3. Ensure Python and dependencies are installed
4. Check the server logs for startup errors

### Tool calls fail
1. Verify environment variables are set (e.g., GOOGLE_API_KEY for Gemini)
2. Check network connectivity for API-based tools
3. Review stderr logs for detailed error messages

### Import errors
1. Ensure the `app` package is in the Python path
2. Install missing dependencies: `pip install -r requirements.txt`
3. Verify file paths are correct for file-based operations

## References

- [MCP Documentation](https://modelcontextprotocol.io/)
- [FastMCP Framework](https://modelcontextprotocol.io/docs/develop/build-server)
- [MCP Debugging Guide](https://modelcontextprotocol.io/legacy/tools/debugging)

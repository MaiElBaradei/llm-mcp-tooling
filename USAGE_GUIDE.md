# AI QA Engineers Assignment - Usage Guide

A comprehensive MCP (Model Context Protocol) client with multiple servers for text summarization, PDF extraction, language detection, weather fetching, and exchange rate conversion.

## Table of Contents

- [Installation](#installation)
- [Starting MCP Servers](#starting-mcp-servers)
- [Running the Client](#running-the-client)
- [Running Playwright Tests](#running-playwright-tests)
- [Sample Requests](#sample-requests)
- [Example Inputs and Outputs](#example-inputs-and-outputs)

---

## Installation

### Prerequisites

- Python 3.10 or higher
- Docker installed and running
- Docker Compose (usually comes with Docker)
- Git

### Step 1: Install uv Package Manager (Recommended)

`uv` is a fast Python package installer and resolver. Install it using one of the following methods:


**Using pip:**
```bash
pip install uv
```

**Verify installation:**
```bash
uv --version
```

**Alternative:** If you prefer not to use `uv`, you can use Python's built-in `venv` and `pip` instead.

### Step 2: Navigate to Project

```bash
cd "/path/to/project"
```

### Step 3: Set Up Virtual Environment

Using `uv` (recommended):

```bash
# Create a virtual environment
uv venv

# Activate the virtual environment
# On Windows:
.venv\Scripts\activate

# On macOS/Linux:
source .venv/bin/activate
```

Or using Python's built-in venv:

```bash
# Create a virtual environment
python -m venv .venv

# Activate the virtual environment
# On Windows:
.venv\Scripts\activate

# On macOS/Linux:
source .venv/bin/activate
```

**Note:** The virtual environment should be activated for all subsequent commands.

### Step 4: Install Dependencies

Using `uv` (recommended):

```bash
uv sync
```

Or using pip:

```bash
pip install -r requirements.txt
```

### Step 5: Set Environment Variables

Add `.env` file sent in email in the project root.

You can use `.env.example` as reference.

### Step 6: Install Playwright Browsers (for tests)

```bash
uv run playwright install firefox
```

---

## Running the LLM Invocation Layer

The LLM invocation layer (`app/llm_invocation_layer/`) provides the core logic for invoking language models with tools. You can use it standalone or as part of the MCP client.

### Direct Script Execution

Run the main application script directly:

```bash
uv run python app/main.py
```

This will:
1. Initialize logging
2. Prompt you for a query
3. Process the query using the LLM invocation layer
4. Return the result

**Example interaction:**

```
Enter your query: What is the weather like in London?
[LLM response with tool execution details]
```


### Component Files

- **`invoke_llm.py`** - Main entry point for LLM invocation
- **`llm_invocation_with_agent.py`** - Agent-based execution strategy
- **`tool_function_definitions.py`** - Tool definitions and schemas
- **`tool_wrappers.py`** - Tool wrapper utilities
- **`llm_invocation_prompt.py`** - Prompt templates and formatting

### Configuration

The invocation layer uses:
- **GOOGLE API** - Configured via `GOOGLE_API_KEY` environment variable
- **Tool Definitions** - Loaded from `tool_function_definitions.py`
- **Prompts** - Defined in `llm_invocation_prompt.py`

### Troubleshooting

**Issue: "No module named 'app'"**
- Solution: Ensure you're running from the project root directory and the virtual environment is activated

**Issue: "GOOGLE_API_KEY not set"**
- Solution: Check your `.env` file contains the API key and it's properly formatted


### Examle Inputs and Output

```
Enter your query: Summarize this document: 
https://proceedings.neurips.cc/paper_files/paper/2017/file/3f5ee243547dee91fbd053c1c4a845aa-Paper.pdf


```


```
Enter your query: What is the weather like in london?


```

```
Enter your query: What is the exchange rate of usd to egp?

```

```
Enter your query: given that this is the ground truth: "Artificial intelligence (AI) is a branch of computer science that focuses on creating systems capable of performing tasks that typically require human intelligence, such as learning, reasoning, and problem solving." and this is the response of an LLM: "Artificial intelligence is a field of computer science concerned with building systems that can perform tasks like learning, reasoning, and problem solving, which normally require human intelligence." evluate the llm response.


2026-01-03 12:09:02,121 | tools.evaluate_llm.evaluate_llm_service_responses | INFO | Evaluation metrics computed: cosine=0.518, lexical=0.410, conciseness=1.000

2026-01-03 12:09:04,798 | tools.hallucination_checker.hallucination_checker | INFO | Hallucination check completed successfully
{"result": {"has_hallucination": false, "hallucinated_statements": [], "explanation": "The response accurately reflects the information provided in the ground truth."}, "prompt": {"system": "\nYou are a fact-checking system.\n\nYour task:\n- Compare the RESPONSE against the GROUND TRUTH.\n- Identify any statements in the RESPONSE that are NOT supported by the GROUND TRUTH.\n- Do NOT infer or assume facts.\n- If all information is supported, return has_hallucination = false.\n\nReturn ONLY valid JSON.\n", "user": "\nGROUND TRUTH:\nArtificial intelligence (AI) is a branch of computer science that focuses on creating systems capable of performing tasks that typically require human intelligence, such as learning, reasoning, and problem solving.\n\nRESPONSE:\nArtificial intelligence is a field of computer science concerned with building systems that can perform tasks like learning, reasoning, and problem solving, which normally require human intelligence.\n\nReturn JSON in the following format:\n{\n  \"has_hallucination\": true | false,\n  \"hallucinated_statements\": [\"...\"],\n  \"explanation\": \"...\"\n}\n"}, "metadata": {"checked_at": "2026-01-03T10:09:04.798424+00:00", "model": "gemini"}}

LLM response: Both evaluations are complete. The LLM response has a cosine similarity of 0.518 and a lexical similarity of 0.410, with a conciseness score of 1. The hallucination check confirms that the response does not contain any information not supported by the ground truth.
```

```
Enter your query: given that this is the ground truth: "Python is a programming language created by Guido van Rossum." and this is the response of an LLM: "Python is a programming language created by Guido van Rossum.
Python is a programming language created by Guido van Rossum in 1989 at the National Research Institute for Mathematics and Computer Science in the Netherlands." evluate the llm response.
```

---

## Starting MCP Servers

MCP (Model Context Protocol) servers expose tools that the client can call. There are three main servers:

### Option A: Using Docker Compose (Recommended)

#### Start All Servers

```bash
docker-compose up
```

#### View Server Logs

```bash
# View all server logs
docker-compose logs -f

# View specific server logs
docker-compose logs -f summarization-server
docker-compose logs -f external-api-server
docker-compose logs -f evaluation-server
```

#### Stop All Servers

```bash
docker-compose down
```

To also remove volumes:

```bash
docker-compose down -v
```

---

### Option B: Manual Server Startup (Alternative)

If you prefer not to use Docker, start each server manually in separate terminal windows.

#### 1. **Summarization Server**

Provides tools for:
- `summarize_text` - Summarize any text
- `summarize_pdf` - Summarize PDF documents
- `extract_pdf_text` - Extract text from PDFs
- `detect_language` - Detect text language

**Terminal 1:**

```bash
uv run python mcp_servers/summarization_server.py
```

**Expected output:**
```
Starting Summarization Server on port 8000...
```

#### 2. **External API Server**

Provides tools for:
- `fetch_weather` - Get weather information for a city
- `fetch_exchange_rate` - Get currency exchange rates

**Terminal 2:**

```bash
uv run python mcp_servers/external_api_server.py
```

#### 3. **Evaluation Server**

Provides tools for:
- `evaluate_llm_responses` - Evaluate LLM output quality
- `hallucination_checker` - Check for hallucinated content

**Terminal 3:**

```bash
uv run python mcp_servers/evaluation_server.py
```

---

## Running the Client

The client connects to all MCP servers and provides an interactive interface with both LLM-powered and manual tool calling.

### Start the Client

#### Prerequisites
- Ensure MCP Servers are running either by [Option A](#option-a-using-docker-compose-recommended) or [Option B](#option-b-manual-server-startup-alternative) before running the tests.

- Run the following commands in the project root (first time only):
```bash
pip install -e .
```

#### Run the Client
```bash
python -m mcp_client
```

### Expected Startup Output

```
========================================
🚀 MCP Client Ready!
========================================

📖 USAGE INSTRUCTIONS
...
```

### Client Commands

#### **LLM-Powered Queries** (Recommended)

Type natural language questions and the Gemini AI will automatically select and call the right tools:

```
💬 Query: Summarize this text: "Artificial intelligence is..."
```

Examples:
- `"Summarize this: [your text]"`
- `"What is the weather in London?"`
- `"Convert 100 USD to EUR"`
- `"Detect the language of: Bonjour"`
- `"Is this response hallucinated? Ground truth: ... Response: ..."`

#### **Manual Tool Calls**

Directly call specific tools with exact parameters:

```
💬 Query: manual
```

Then:
1. Select the tool by number or name
2. Enter required parameters when prompted
3. View the result

#### **Special Commands**

| Command | Description |
|---------|-------------|
| `tools` | List all available tools |
| `manual-list` | Show detailed tool information |
| `help` | Display help menu |
| `quit` | Exit the client |



---

## Sample Requests

### Example 1: Summarize Text

**Interactive Client:**

```
💬 Query: Summarize this text: "Artificial intelligence (AI) is intelligence demonstrated by machines, in contrast to the natural intelligence displayed by animals and humans. AI research has been defined as the field of study of intelligent agents. The term 'Artificial Intelligence' was coined in 1956."

🤔 Thinking...

🤖 Response:
{
  "summary": "Artificial intelligence (AI) is machine-based intelligence that differs from natural intelligence in humans and animals. The field was formally established in 1956.",
  "metadata": {
    "document_length": 274,
    "summary_length": 128,
    "model_name": "gemini-2.5-flash",
    "processing_time": 1.23
  }
}
```

**Manual Tool Call:**

```
💬 Query: manual

Available tools:
  1. summarize_text
  2. detect_language
  3. fetch_weather
  ...

Select tool (number or name): summarize_text

🔹 text
   Type: string
   Description: The text to summarize
   Enter value (Required): Your text here...
```

### Example 2: Fetch Weather

```
💬 Query: What is the weather in New York?

🤔 Thinking...

🤖 Response:
{
  "data": {
    "city": "New York",
    "temperature_celsius": 8.5,
    "wind_speed_kmh": 12.3,
    "condition": "Cloudy"
  },
  "metadata": {
    "provider": "OpenWeatherMap",
    "timestamp": "2026-01-02T15:30:00Z"
  }
}
```

### Example 3: Detect Language

```
💬 Query: Detect the language of: "Bonjour, comment allez-vous?"

🤔 Thinking...

🤖 Response:
{
  "language": "fr",
  "confidence": 0.98,
  "language_name": "French"
}
```

### Example 4: Check for Hallucinations

```
💬 Query: Check if this is hallucinated. Ground truth: "Paris is the capital of France." Response: "Paris is located in France and is known as the City of Light."

🤔 Thinking...

🤖 Response:
{
  "has_hallucination": false,
  "hallucinated_statements": [],
  "explanation": "The response is factually accurate and consistent with the ground truth."
}
```

### Example 5: Extract PDF Text

```
💬 Query: Extract text from: https://example.com/document.pdf

🤔 Thinking...

🤖 Response:
{
  "success": True,
  "text": "Document content here...",
  "pages": pages,
  "error": None
}

```

---

## Example Inputs and Outputs

### Summarize Text Tool

**Input:**
```json
{
  "text": "Machine learning is a subset of artificial intelligence that enables systems to learn and improve from experience without being explicitly programmed. It focuses on the development of computer programs that can access data and use it to learn for themselves."
}
```

**Output:**
```json
{
  "summary": "Machine learning is a subset of AI that allows systems to learn from data and improve automatically without explicit programming.",
  "prompt": {
    "system_prompt": "You are a concise summarization assistant...",
    "user_prompt": "Summarize the following text: ..."
  },
  "metadata": {
    "document_length": 210,
    "summary_length": 98,
    "model_name": "gemini-2.5-flash",
    "processing_time": 1.45
  }
}
```

### Detect Language Tool

**Input:**
```json
{
  "text": "Buenos días, ¿cómo estás?"
}
```

**Output:**
```json
{
  "language": "es",
  "language_name": "Spanish",
  "confidence": 0.95
}
```

### Fetch Weather Tool

**Input:**
```json
{
  "city": "London"
}
```

**Output:**
```json
{
  "data": {
    "city": "London",
    "temperature_celsius": 5.2,
    "wind_speed_kmh": 8.5,
    "condition": "Rainy"
  },
  "metadata": {
    "provider": "OpenWeatherMap",
    "endpoint": "/weather",
    "timestamp": "2026-01-02T15:35:22Z"
  }
}
```

### Fetch Exchange Rate Tool

**Input:**
```json
{
  "base_currency": "USD",
  "target_currency": "EUR"
}
```

**Output:**
```json
{
  "data": {
    "base_currency": "USD",
    "target_currency": "EUR",
    "exchange_rate": 0.92
  },
  "metadata": {
    "provider": "ExchangeRate API",
    "endpoint": "/latest",
    "timestamp": "2026-01-02T15:35:22Z"
  }
}
```

### Hallucination Checker Tool

**Input:**
```json
{
  "ground_truth": "The Great Wall of China is approximately 13,000 miles long.",
  "response": "The Great Wall of China stretches for about 13,000 miles across northern China."
}
```

**Output:**
```json
{
  "result": {
    "has_hallucination": false,
    "hallucinated_statements": [],
    "explanation": "The response accurately reflects the ground truth information."
  },
  "prompt": {...},
  "metadata": {...}
}
```

---

## Running Playwright Tests

Playwright tests automate browser interactions with Wikipedia to extract content and send it to the MCP Summarization server.

### Prerequisites

- Ensure MCP Servers are running either by [Option A](#option-a-using-docker-compose-recommended) or [Option B](#option-b-manual-server-startup-alternative) before running the tests.

- Ensure Firefox browser is installed:

```bash
uv run playwright install firefox
```

### Run All Tests

```bash
uv run pytest tests/ --browser firefox -v -s
```

### Run Specific Test

**Baseline test** (recommended - comprehensive end-to-end flow):

```bash
uv run pytest tests/test_wikipedia_mcp_summarization.py
```

**Other tests:**

```bash
#Invalid tool response
uv run pytest tests/test_invalid_tool_response.py
```

```bash
#Missing of empty content
uv run pytest tests/test_missing_or_empty_content.py
```

---

## Troubleshooting

### Issue: "GOOGLE_API_KEY not found"

**Solution:** Ensure your `.env` file contains:
```env
GOOGLE_API_KEY= "API_KEY sent in .env file"
```
### Issue: "EXCHANGE_RATE_API_KEY not found"

**Solution:** Ensure your `.env` file contains:
```env
EXCHANGE_RATE_API_KEY= "API_KEY sent in .env file"
```
### Issue: "OPEN_WEATHER_MAP_API_KEY not found"

**Solution:** Ensure your `.env` file contains:
```env
OPEN_WEATHER_MAP_API_KEY= "API_KEY sent in .env file"
```



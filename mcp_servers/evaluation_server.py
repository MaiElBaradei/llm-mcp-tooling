#!/usr/bin/env python3
"""
MCP Evaluation Tool Server

Exposes tools for:
- evaluate_llm_responses
- hallucination_checker
"""

import logging
from fastmcp import FastMCP
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Configure logging to stderr (not stdout, as that breaks STDIO communication)
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s | %(name)s | %(levelname)s | %(message)s',
    handlers=[logging.StreamHandler()]
)
logger = logging.getLogger(__name__)

# Initialize FastMCP server
mcp = FastMCP("evaluation-server")

# Import tools
from app.tools import (
    EvaluateLLMResponsesTool,
    HallucinationCheckerTool,
)


@mcp.tool()
async def evaluate_llm_responses(ground_truth: str, response: str) -> str:
    """Evaluate an LLM response against ground truth using multiple metrics.
    
    Uses cosine similarity, lexical similarity, and conciseness scoring.
    
    Args:
        ground_truth: The reference text to compare against
        response: The LLM response to evaluate
        
    Returns:
        Similarity scores (cosine, lexical, conciseness) and metadata
    """
    try:
        tool = EvaluateLLMResponsesTool()
        result = tool.run({"ground_truth": ground_truth, "response": response})
        return str(result)
    except Exception as e:
        return f"Error evaluating LLM responses: {str(e)}"


@mcp.tool()
async def hallucination_checker(ground_truth: str, response: str) -> str:
    """Check whether the response contains information not supported by ground truth.
    
    Args:
        ground_truth: The factual reference text
        response: The response text to check for hallucinations
        
    Returns:
        Boolean indicating if hallucination exists, list of hallucinated statements, 
        explanation, and metadata
    """
    try:
        tool = HallucinationCheckerTool()
        result = tool.run({"ground_truth": ground_truth, "response": response})
        return str(result)
    except Exception as e:
        return f"Error checking for hallucinations: {str(e)}"


def main():
    """Initialize and run the MCP server with SSE."""
    port = int(os.getenv("SERVER_PORT", "8000"))
    logger.info(f"Starting Evaluation Tool Server on port {port}...")
    mcp.run(transport="sse", port=port, host="0.0.0.0")


if __name__ == "__main__":
    main()

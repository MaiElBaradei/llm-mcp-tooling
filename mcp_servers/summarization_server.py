#!/usr/bin/env python3
"""
MCP Summarization Server

Exposes tools for:
- extract_pdf_text
- summarize_text
- summarize_pdf
- detect_language
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import logging
from mcp.server.fastmcp import FastMCP

# Configure logging to stderr (not stdout, as that breaks STDIO communication)
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s | %(name)s | %(levelname)s | %(message)s',
    handlers=[logging.StreamHandler()]
)
logger = logging.getLogger(__name__)

# Initialize FastMCP server
mcp = FastMCP("summarization-server")

# Import tools
from app.tools import (
    ExtractPDFTextTool,
    SummarizeTextTool,
    SummarizePDFTool,
    DetectLanguageTool,
)


@mcp.tool()
async def extract_pdf_text(pdf_path_or_url: str) -> str:
    """Extract text from a PDF file given a local path or HTTP URL.
    
    Args:
        pdf_path_or_url: Local file path or HTTP URL to the PDF file
        
    Returns:
        Extracted text and number of pages
    """
    try:
        tool = ExtractPDFTextTool()
        result = tool.run(pdf_path_or_url)
        return str(result)
    except Exception as e:
        return f"Error extracting PDF text: {str(e)}"


@mcp.tool()
async def summarize_text(text: str) -> str:
    """Summarize a given text using an LLM.
    
    Args:
        text: The text to summarize
        
    Returns:
        Summary along with prompt and metadata information
    """
    try:
        tool = SummarizeTextTool()
        result = tool.run(text)
        return str(result)
    except Exception as e:
        return f"Error summarizing text: {str(e)}"


@mcp.tool()
async def summarize_pdf(file_path: str) -> str:
    """Summarize the content of a PDF file from a local path or HTTP URL.
    
    Args:
        file_path: Local file path or HTTP URL to the PDF file
        
    Returns:
        Summary of the PDF document with metadata
    """
    try:
        tool = SummarizePDFTool()
        # Consume the generator and return the final summary
        summary_text = ""
        for chunk in tool.run(file_path):
            if isinstance(chunk, dict) and "partial_summary" in chunk:
                summary_text += chunk["partial_summary"]
            elif isinstance(chunk, dict) and "final_summary" in chunk:
                summary_text = chunk["final_summary"]
        return summary_text if summary_text else "PDF summary could not be generated."
    except Exception as e:
        return f"Error summarizing PDF: {str(e)}"


@mcp.tool()
async def detect_language(text: str) -> str:
    """Detect the language of a given text string.
    
    Args:
        text: The text to analyze
        
    Returns:
        ISO 639-1 language code and confidence score
    """
    try:
        tool = DetectLanguageTool()
        result = tool.run(text)
        return str(result)
    except Exception as e:
        return f"Error detecting language: {str(e)}"


def main():
    """Initialize and run the MCP server."""
    logger.info("Starting Summarization Server...")
    mcp.run(transport="stdio")


if __name__ == "__main__":
    main()

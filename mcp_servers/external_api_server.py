#!/usr/bin/env python3
"""
MCP External API Tooling Server

Exposes tools for:
- fetch_weather
- fetch_exchange_rate
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
mcp = FastMCP("external-api-server")

# Import tools
from app.tools import (
    FetchWeatherTool,
    FetchExchangeRateTool,
)


@mcp.tool()
async def fetch_weather(city: str) -> str:
    """Retrieve current weather information for a given city.
    
    Args:
        city: Name of the city to fetch weather for
        
    Returns:
        Temperature in Celsius, wind speed in km/h, condition, and metadata
    """
    try:
        tool = FetchWeatherTool()
        result = tool.run(city)
        return str(result)
    except Exception as e:
        return f"Error fetching weather: {str(e)}"


@mcp.tool()
async def fetch_exchange_rate(base_currency: str, target_currency: str) -> str:
    """Retrieve the latest exchange rate for a currency pair.
    
    Args:
        base_currency: The base currency code (e.g., 'USD')
        target_currency: The target currency code (e.g., 'EUR')
        
    Returns:
        Exchange rate along with provider and timestamp metadata
    """
    try:
        tool = FetchExchangeRateTool()
        result = tool.run(base_currency, target_currency)
        return str(result)
    except Exception as e:
        return f"Error fetching exchange rate: {str(e)}"


def main():
 """Initialize and run the MCP server with SSE."""
 port = int(os.getenv("SERVER_PORT", "8000"))
 logger.info(f"Starting External API Tooling Server on port {port}...")
 mcp.run(transport="sse", port=port, host="0.0.0.0")


if __name__ == "__main__":
    main()

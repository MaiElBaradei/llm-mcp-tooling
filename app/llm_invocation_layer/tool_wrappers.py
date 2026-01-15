from typing import Iterator, Dict
from langgraph.config import get_stream_writer 
from langchain.tools import tool
from tools import (
    ExtractPDFTextTool, 
    EXTRACT_PDF_ARGS_SCHEMA,
    DetectLanguageTool,
    DETECT_LANGUAGE_ARGS_SCHEMA,
    FetchWeatherTool,
    FETCH_WEATHER_ARGS_SCHEMA,
    FetchExchangeRateTool,
    FETCH_EXCHANGE_RATE_ARGS_SCHEMA,
    SummarizeTextTool,
    SUMMARIZE_TEXT_ARGS_SCHEMA,
    HallucinationCheckerTool,
    HALLUCINATION_CHECKER_ARGS_SCHEMA,
    SummarizePDFTool,
    SUMMARIZE_PDF_ARGS_SCHEMA,
    EvaluateLLMResponsesTool,
    EVALUATION_INPUT_SCHEMA,
)

@tool("extract_pdf_text", args_schema=EXTRACT_PDF_ARGS_SCHEMA)
def extract_pdf_tool(pdf_path_or_url: str) -> dict:
    """Extracts text from a PDF file given a local path or HTTP URL.
    
    Returns extracted text and number of pages.
    
    Args:
        pdf_path_or_url: Local file path or HTTP URL to the PDF file
    """
    return ExtractPDFTextTool().run(pdf_path_or_url)


@tool("detect_language", args_schema=DETECT_LANGUAGE_ARGS_SCHEMA)
def detect_language_tool(text: str) -> dict:
    """Detects the language of a given text string.
    
    Returns the ISO 639-1 language code and confidence score.
    
    Args:
        text: The text string to analyze
    """
    return DetectLanguageTool().run(text)


@tool("fetch_weather", args_schema=FETCH_WEATHER_ARGS_SCHEMA)
def fetch_weather_tool(city: str) -> dict:
    """Retrieves current weather information for a given city.
    
    Returns temperature, wind speed, condition, and metadata.
    
    Args:
        city: Name of the city to fetch weather for
    """
    return FetchWeatherTool().run(city)


@tool("fetch_exchange_rate", args_schema=FETCH_EXCHANGE_RATE_ARGS_SCHEMA)
def fetch_exchange_rate_tool(base_currency: str, target_currency: str) -> dict:
    """Retrieves the latest exchange rate for a currency pair.
    
    Returns the exchange rate along with provider and timestamp metadata.
    
    Args:
        base_currency: The base currency code (e.g., 'USD')
        target_currency: The target currency code (e.g., 'EUR')
    """
    return FetchExchangeRateTool().run(base_currency, target_currency)


@tool("summarize_text", args_schema=SUMMARIZE_TEXT_ARGS_SCHEMA)
def summarize_text_tool(text: str) -> dict:
    """Summarizes a given text using an LLM.
    
    Returns a summary along with prompt and metadata information.
    
    Args:
        text: The text content to summarize
    """
    return SummarizeTextTool().run(text)


@tool("hallucination_checker", args_schema=HALLUCINATION_CHECKER_ARGS_SCHEMA)
def hallucination_checker_tool(ground_truth: str, response: str) -> dict:
    """Checks whether the response contains information not supported by the given ground truth.
    
    Args:
        ground_truth: The factual reference text
        response: The response text to check for hallucinations
    """
    return HallucinationCheckerTool().run({"ground_truth": ground_truth, "response": response})


@tool("summarize_pdf", args_schema=SUMMARIZE_PDF_ARGS_SCHEMA)
def summarize_pdf_tool(file_path: str) -> Iterator[Dict]:
    """Summarizes the content of a PDF file from a local path or HTTP URL.
    
    Returns a streaming summary of the PDF document.
    
    Args:
        file_path: Local file path or HTTP URL to the PDF file
    """
    writer = get_stream_writer()
    for event in SummarizePDFTool().run(file_path):
        writer(event)
    return event["final_summary"]


@tool("evaluate_llm_responses", args_schema=EVALUATION_INPUT_SCHEMA)
def evaluate_llm_responses_tool(ground_truth: str, response: str) -> dict:
    """Evaluates an LLM response against ground truth using cosine similarity, lexical similarity, and conciseness.
    
    Args:
        ground_truth: The reference text to compare against
        response: The LLM response to evaluate
    """
    return EvaluateLLMResponsesTool().run({"ground_truth": ground_truth, "response": response})




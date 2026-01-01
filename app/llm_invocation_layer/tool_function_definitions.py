"""
Function definitions for Gemini function calling.
Converts our tools into Gemini's function calling format.
"""

def get_tools_function_definitions() -> list:
    """
    Returns a list of function definitions in Gemini's function calling format.
    Each function definition describes a tool that the LLM can call.
    """
    return [
        {
            "name": "fetch_weather",
            "description": "Retrieves current weather information for a given city. Returns temperature in Celsius, wind speed in km/h, condition, and metadata.",
            "parameters": {
                "type": "object",
                "properties": {
                    "city": {
                        "type": "string",
                        "description": "The name of the city"
                    }
                },
                "required": ["city"]
            }
        },
        {
            "name": "fetch_exchange_rate",
            "description": "Retrieves the latest exchange rate for a currency pair. Returns exchange rate, provider, and timestamp. Currency codes must be valid ISO 4217 codes (3 letters, uppercase).",
            "parameters": {
                "type": "object",
                "properties": {
                    "base_currency": {
                        "type": "string",
                        "description": "Base currency code (e.g., 'USD', 'EUR')"
                    },
                    "target_currency": {
                        "type": "string",
                        "description": "Target currency code (e.g., 'USD', 'EUR')"
                    }
                },
                "required": ["base_currency", "target_currency"]
            }
        },
        {
            "name": "summarize_pdf",
            "description": "Summarizes the content of a PDF file from a local path or HTTP URL. Returns a streaming summary of the PDF document with metadata. File must exist locally or URL must be accessible.",
            "parameters": {
                "type": "object",
                "properties": {
                    "pdf_path_or_url": {
                        "type": "string",
                        "description": "Local file path or HTTP URL to PDF"
                    }
                },
                "required": ["pdf_path_or_url"]
            }
        },
        {
            "name": "summarize_text",
            "description": "Summarizes a given text using an LLM. Returns summary, prompt details, and metadata including document length, summary length, processing time. Text must not be empty.",
            "parameters": {
                "type": "object",
                "properties": {
                    "text": {
                        "type": "string",
                        "description": "The text to summarize"
                    }
                },
                "required": ["text"]
            }
        },
        {
            "name": "extract_pdf_text",
            "description": "Extracts text from a PDF file given a local path or HTTP URL. Returns extracted text and number of pages. File must exist locally or URL must be accessible.",
            "parameters": {
                "type": "object",
                "properties": {
                    "source": {
                        "type": "string",
                        "description": "Local file path or HTTP URL to PDF"
                    }
                },
                "required": ["source"]
            }
        },
        {
            "name": "detect_language",
            "description": "Detects the language of a given text string. Returns ISO 639-1 language code and confidence score. Text must not be empty.",
            "parameters": {
                "type": "object",
                "properties": {
                    "text": {
                        "type": "string",
                        "description": "The text to analyze"
                    }
                },
                "required": ["text"]
            }
        },
        {
            "name": "Evaluate_llm_responses",
            "description": "Evaluates an LLM response against ground truth using cosine similarity, lexical similarity, and conciseness. Returns similarity scores and metadata. Both ground_truth and response must be non-empty strings.",
            "parameters": {
                "type": "object",
                "properties": {
                    "ground_truth": {
                        "type": "string",
                        "description": "The expected correct response"
                    },
                    "response": {
                        "type": "string",
                        "description": "The LLM response to evaluate"
                    }
                },
                "required": ["ground_truth", "response"]
            }
        },
        {
            "name": "hallucination_checker",
            "description": "Checks whether the response contains information not supported by the given ground truth. Returns boolean indicating if hallucination exists, list of hallucinated statements, explanation, and metadata. Both ground_truth and response must be non-empty strings.",
            "parameters": {
                "type": "object",
                "properties": {
                    "ground_truth": {
                        "type": "string",
                        "description": "The reference truth"
                    },
                    "response": {
                        "type": "string",
                        "description": "The response to check for hallucinations"
                    }
                },
                "required": ["ground_truth", "response"]
            }
        }
    ]


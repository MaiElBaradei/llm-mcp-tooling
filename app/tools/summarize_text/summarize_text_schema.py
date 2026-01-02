# JSON Schema definitions for summarize_text tool

SUMMARIZE_TEXT_ARGS_SCHEMA = {
    "type": "object",
    "required": ["text"],
    "properties": {
        "text": {
            "type": "string",
            "description": "The text to summarize"
        }
    }
}

SUMMARIZE_TEXT_OUTPUT_SCHEMA = {
    "type": "object",
    "required": ["summary", "prompt", "metadata"],
    "properties": {
        "summary": {
            "type": "string"
        },
        "prompt": {
            "type": "object",
            "required": ["system_prompt", "user_prompt"],
            "properties": {
                "system_prompt": {
                    "type": "string"
                },
                "user_prompt": {
                    "type": "string"
                }
            }
        },
        "metadata": {
            "type": "object",
            "required": ["model_name", "document_language", "document_length", "summary_length", "processing_time"],
            "properties": {
                "model_name": {
                    "type": "string"
                },
                "document_language": {
                    "type": "string"
                },
                "document_length": {
                    "type": "integer"
                },
                "summary_length": {
                    "type": "integer"
                },
                "processing_time": {
                    "type": "number"
                }
            }
        }
    }
}
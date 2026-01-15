# JSON Schema definitions for detect_language tool

DETECT_LANGUAGE_ARGS_SCHEMA = {
    "type": "object",
    "required": ["text"],
    "properties": {
        "text": {
            "type": "string",
            "description": "The text to detect language for"
        }
    }
}
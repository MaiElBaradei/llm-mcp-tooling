# JSON Schema definitions for summarize_pdf tool

SUMMARIZE_PDF_ARGS_SCHEMA = {
    "type": "object",
    "required": ["file_path"],
    "properties": {
        "file_path": {
            "type": "string",
            "description": "Local file path or HTTP URL to the PDF file"
        }
    }
}

SUMMARIZE_PDF_STREAM_OUTPUT_SCHEMA = {
    "type": "object",
    "properties": {
        "chunk": {
            "type": "integer",
            "description": "Chunk number in the streaming output"
        },
        "partial_summary": {
            "type": "string",
            "description": "Partial summary for the current chunk"
        },
        "final_summary": {
            "type": "string",
            "description": "Final complete summary of the PDF"
        },
        "metadata": {
            "oneOf": [
                {
                    "type": "object",
                    "description": "Single metadata object"
                },
                {
                    "type": "array",
                    "items": {
                        "type": "object"
                    },
                    "description": "List of metadata objects"
                }
            ]
        }
    }
}
    



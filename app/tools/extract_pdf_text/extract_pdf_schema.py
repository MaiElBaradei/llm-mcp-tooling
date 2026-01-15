# JSON Schema definitions for extract_pdf_text tool

EXTRACT_PDF_ARGS_SCHEMA = {
    "type": "object",
    "required": ["source"],
    "properties": {
        "source": {
            "type": "string",
            "description": "Local file path or HTTP URL to the PDF file"
        }
    }
}
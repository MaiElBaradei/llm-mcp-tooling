from pydantic import BaseModel
from typing import List


class prompt(BaseModel):
    system_prompt: str
    user_prompt: str

class metadata(BaseModel):
    model_name: str
    document_language: str
    document_length: int
    summary_length: int
    processing_time: float

class SummarizeTextOutput(BaseModel):
    summary: str
    prompt: prompt
    metadata: metadata



RESPONSE_SCHEMA = {
    "type": "OBJECT",
    "required": ["summary", "prompt", "metadata"],
    "properties": {
        "summary": {"type": "STRING"},
        "prompt": {
            "type": "OBJECT",
            "required": ["system_prompt", "user_prompt"],
            "properties": {
                "system_prompt": {"type": "STRING"},
                "user_prompt": {"type": "STRING"},
            },
        },
        "metadata": {
            "type": "OBJECT",
            "required": ["model_name", "document_language", "document_length", "summary_length", "processing_time"],
            "properties": {
                "model_name": {"type": "STRING"},
                "document_language": {"type": "STRING"},
                "document_length": {"type": "INTEGER"},
                "summary_length": {"type": "INTEGER"},
                "processing_time": {"type": "NUMBER"},
            },
        },
    },
}
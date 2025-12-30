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
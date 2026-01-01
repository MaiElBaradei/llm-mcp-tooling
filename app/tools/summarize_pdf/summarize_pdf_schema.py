from pydantic import BaseModel, validator
from typing import Optional, Dict, Any, List

class SummarizePDFToolArgs(BaseModel):
    file_path: str

class SummarizePDFStreamOutput(BaseModel):
    chunk: Optional[int] = None
    partial_summary: Optional[str] = None
    final_summary: Optional[str] = None
    # Accept either a single dict or a list of dicts. Validator normalizes to list.
    metadata: Optional[List[Dict[str, Any]]] = None

    @validator("metadata", pre=True)
    def _normalize_metadata(cls, v):
        if v is None:
            return None
        # If a single dict is provided, wrap it in a list
        if isinstance(v, dict):
            return [v]
        # If already a list (of dicts), accept as-is
        if isinstance(v, list):
            return v
        raise ValueError("metadata must be a dict or list of dicts")
    



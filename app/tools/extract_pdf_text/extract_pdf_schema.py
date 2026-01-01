from pydantic import BaseModel

class ExtractPDFToolArgs(BaseModel):
    source: str
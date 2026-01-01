from pydantic import BaseModel

class DetectLanguageToolArgs(BaseModel):
    text: str
from typing import Optional

_LANGUAGE_CHUNK_MAP = {
    "en": 600,
    "es": 600,
    "fr": 600,
    "de": 600,
    "ar": 500,
    # Use smaller sizes for CJK when using character-based splitting
    "zh": 300,
    "ja": 300,
    "ko": 300,
}

def decide_chunk_size(language: Optional[str], default: int = 600) -> int:
    if not language:
        return default
    lang = language.split("-")[0].lower()
    return _LANGUAGE_CHUNK_MAP.get(lang, default)
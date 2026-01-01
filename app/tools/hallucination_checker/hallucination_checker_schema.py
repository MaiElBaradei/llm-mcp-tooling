from pydantic import BaseModel

# Pydantic Schema definitions for hallucination_checker tool input
    
class HallucinationCheckerToolArgs(BaseModel):
    ground_truth: str
    response: str

# JSON Schema definitions for hallucination_checker tool

HALLUCINATION_INPUT_SCHEMA = {
    "type": "object",
    "required": ["ground_truth", "response"],
    "properties": {
        "ground_truth": {
            "type": "string",
            "minLength": 1
        },
        "response": {
            "type": "string",
            "minLength": 1
        }
    }
}

HALLUCINATION_RESULT_SCHEMA = {
    "type": "object",
    "required": ["has_hallucination", "hallucinated_statements", "explanation"],
    "properties": {
        "has_hallucination": {
            "type": "boolean"
        },
        "hallucinated_statements": {
            "type": "array",
            "items": {
                "type": "string"
            }
        },
        "explanation": {
            "type": "string"
        }
    }
}

HALLUCINATION_OUTPUT_SCHEMA = {
    "type": "object",
    "required": ["result", "prompt", "metadata"],
    "properties": {
        "result": HALLUCINATION_RESULT_SCHEMA,
        "prompt": {
            "type": "object"
        },
        "metadata": {
            "type": "object"
        }
    }
}

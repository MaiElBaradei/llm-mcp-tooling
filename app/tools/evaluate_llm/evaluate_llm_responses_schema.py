from pydantic import BaseModel

class EvaluateLLMResponsesToolArgs(BaseModel):
    ground_truth: str
    response: str


# JSON Schema definitions for evaluate_llm tool

EVALUATION_INPUT_SCHEMA = {
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

SIMILARITY_SCORES_SCHEMA = {
    "type": "object",
    "required": ["cosine_similarity", "lexical_similarity", "conciseness_score"],
    "properties": {
        "cosine_similarity": {
            "type": "number"
        },
        "lexical_similarity": {
            "type": "number"
        },
        "conciseness_score": {
            "type": "number"
        }
    }
}

EVALUATION_OUTPUT_SCHEMA = {
    "type": "object",
    "required": ["scores", "metadata"],
    "properties": {
        "scores": SIMILARITY_SCORES_SCHEMA,
        "metadata": {
            "type": "object"
        }
    }
}

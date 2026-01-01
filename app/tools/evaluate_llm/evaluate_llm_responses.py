from .evaluate_llm_responses_schema import (
    EVALUATION_INPUT_SCHEMA,
    EVALUATION_OUTPUT_SCHEMA,
)
from .evaluate_llm_service_responses import EvaluateLLMResponsesService
from datetime import datetime, timezone
import logging
import jsonschema

logger = logging.getLogger(__name__)


class EvaluateLLMResponsesTool:
    name = "Evaluate_llm_responses"
    description = (
        "Evaluates an LLM response against ground truth using "
        "cosine similarity, lexical similarity, and conciseness."
    )

    def __init__(self):
        self.service = EvaluateLLMResponsesService()
        logger.info("EvaluateLLMResponsesTool initialized")

    def run(self, input_data: dict) -> dict:
        try:
            logger.info("Starting LLM response evaluation")
            
            # Validate input against JSON schema
            try:
                jsonschema.validate(instance=input_data, schema=EVALUATION_INPUT_SCHEMA)
            except jsonschema.ValidationError as e:
                logger.error(f"Input validation failed: {e.message}")
                raise ValueError(f"Invalid input data: {e.message}")
            
            ground_truth = input_data["ground_truth"]
            response = input_data["response"]
            
            scores = self.service.evaluate(ground_truth, response)

            result = {
                "scores": scores,
                "metadata": {
                    "evaluated_at": datetime.now(timezone.utc).isoformat(),
                    "metrics": ["cosine", "lexical", "conciseness"],
                }
            }
            
            # Validate output against JSON schema
            try:
                jsonschema.validate(instance=result, schema=EVALUATION_OUTPUT_SCHEMA)
            except jsonschema.ValidationError as e:
                logger.error(f"Output validation failed: {e.message}")
                raise ValueError(f"Invalid output data: {e.message}")
            
            logger.info("LLM response evaluation completed successfully")
            return result
        except (ValueError, KeyError) as e:
            logger.error(f"Error evaluating LLM response: {e}", exc_info=True)
            raise
        except Exception as e:
            logger.error(f"Error evaluating LLM response: {e}", exc_info=True)
            raise

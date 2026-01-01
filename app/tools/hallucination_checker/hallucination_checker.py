from datetime import datetime, timezone
from .hallucination_checker_schema import (
    HALLUCINATION_INPUT_SCHEMA,
    HALLUCINATION_OUTPUT_SCHEMA,
)
from .hallucination_checker_service import HallucinationCheckerService
from ...llm.gemini_client import GeminiClient
from .hallucination_checker_prompt import SYSTEM_PROMPT, USER_PROMPT_TEMPLATE
import logging
import jsonschema

logger = logging.getLogger(__name__)


class HallucinationCheckerTool:
    name = "hallucination_checker"
    description = (
        "Checks whether the response contains information "
        "not supported by the given ground truth."
    )

    def __init__(self):
        llm = GeminiClient()
        self.service = HallucinationCheckerService(llm)
        logger.info("HallucinationCheckerTool initialized")

    def run(self, input_data: dict) -> dict:
        try:
            logger.info("Starting hallucination check")
            
            # Validate input against JSON schema
            try:
                jsonschema.validate(instance=input_data, schema=HALLUCINATION_INPUT_SCHEMA)
            except jsonschema.ValidationError as e:
                logger.error(f"Input validation failed: {e.message}")
                raise ValueError(f"Invalid input data: {e.message}")
            
            ground_truth = input_data["ground_truth"]
            response = input_data["response"]
            
            # Generate user prompt for metadata
            user_prompt = USER_PROMPT_TEMPLATE.format(
                ground_truth=ground_truth,
                response=response
            )
            
            output = self.service.check(
                ground_truth=ground_truth,
                response=response
            )

            result = {
                "result": output,
                "prompt": {
                    "system": SYSTEM_PROMPT,
                    "user": user_prompt
                },
                "metadata": {
                    "checked_at": datetime.now(timezone.utc).isoformat(),
                    "model": "gemini",
                }
            }
            
            # Validate output against JSON schema
            try:
                jsonschema.validate(instance=result, schema=HALLUCINATION_OUTPUT_SCHEMA)
            except jsonschema.ValidationError as e:
                logger.error(f"Output validation failed: {e.message}")
                raise ValueError(f"Invalid output data: {e.message}")
            
            logger.info("Hallucination check completed successfully")
            return result
        except (ValueError, KeyError) as e:
            logger.error(f"Error checking hallucination: {e}", exc_info=True)
            raise
        except Exception as e:
            logger.error(f"Error checking hallucination: {e}", exc_info=True)
            raise

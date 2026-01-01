from ...llm import LLMClient
from .hallucination_checker_prompt import SYSTEM_PROMPT, USER_PROMPT_TEMPLATE
from .hallucination_checker_schema import HALLUCINATION_RESULT_SCHEMA
import logging
import inspect

logger = logging.getLogger(__name__)


class HallucinationCheckerService:
    def __init__(self, llm: LLMClient):
        self.llm = llm
        logger.info("HallucinationCheckerService initialized")

    def check(self, ground_truth: str, response: str) -> dict:
        try:
            logger.info("Checking for hallucinations in response")
            user_prompt = USER_PROMPT_TEMPLATE.format(
                ground_truth=ground_truth,
                response=response
            )

            # Check if the LLM client's generate method accepts response_schema parameter
            # by inspecting its signature
            generate_signature = inspect.signature(self.llm.generate)
            params = list(generate_signature.parameters.keys())
            
            if 'response_schema' in params:
                # Client supports schema parameter (e.g., GeminiClient)
                logger.debug("Using LLM client with schema support")
                raw_output = self.llm.generate(
                    system_prompt=SYSTEM_PROMPT,
                    user_prompt=user_prompt,
                    response_schema=HALLUCINATION_RESULT_SCHEMA,
                    response_type="application/json",
                    temperature=0.0
                )
            else:
                # Base interface - no schema support
                logger.warning("LLM client doesn't support schema parameter, using base interface")
                raw_output = self.llm.generate(
                    system_prompt=SYSTEM_PROMPT,
                    user_prompt=user_prompt
                )

            if "json" not in raw_output:
                logger.error("Invalid response from LLM: missing 'json' key")
                raise ValueError("Invalid response from LLM: missing 'json' key")

            result = raw_output["json"]
            logger.info(f"Hallucination check completed: has_hallucination={result.get('has_hallucination', False)}")
            return result
        except Exception as e:
            logger.error(f"Error checking for hallucinations: {e}", exc_info=True)
            raise

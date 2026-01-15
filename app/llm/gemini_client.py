from google.genai import Client, types
from dotenv import load_dotenv
from typing import Dict, List, Optional, Any
from .interfaces import LLMClient
import logging

load_dotenv()

logger = logging.getLogger(__name__)


class GeminiClient(LLMClient):
    """
    Gemini LLM client wrapper.
    """

    def __init__(self, model_name: str = "gemini-2.5-flash-lite"):
        try:
            logger.info(f"Initializing GeminiClient with model: {model_name}")
            self.client = Client()
            self.model = model_name
            logger.info("GeminiClient initialized successfully")
        except Exception as e:
            logger.error(f"Error initializing GeminiClient: {e}", exc_info=True)
            raise

    def generate(self, system_prompt: str, user_prompt: str, response_schema: dict = None, response_type: str = "application/json", temperature: float = 0.0) -> Dict:
        try:
            logger.info(f"Generating content with Gemini model: {self.model}")
            logger.debug(f"System prompt length: {len(system_prompt)}, User prompt length: {len(user_prompt)}")
            
            config = types.GenerateContentConfig(
                system_instruction=system_prompt,
                temperature=temperature,
            )
            
            if response_schema:
                config.response_mime_type = response_type
                config.response_schema = response_schema
            
            response = self.client.models.generate_content(
                model=self.model,
                config=config,
                contents=user_prompt,
            )

            if not response or not hasattr(response, 'parsed'):
                logger.error("Invalid response from Gemini API: missing parsed content")
                raise ValueError("Invalid response from Gemini API: missing parsed content")

            result = {
                "json": response.parsed,
                "model": self.model,
            }
            logger.info("Content generated successfully by Gemini")
            return result
        except Exception as e:
            logger.error(f"Error generating content with Gemini: {e}", exc_info=True)
            raise

    def generate_with_function_calling(
        self,
        system_prompt: str,
        user_prompt: str,
        tools: List[Dict[str, Any]],
        conversation_history: Optional[List[Any]] = None,
        temperature: float = 0.0,
        send_tools: bool = True
    ) -> Dict:
        """
        Generate content with function calling support.
        
        Args:
            system_prompt: System instruction for the LLM
            user_prompt: User's natural language prompt (only on first call)
            tools: List of function definitions in Gemini format
            conversation_history: Previous conversation turns (model responses and function results)
            temperature: Sampling temperature
            
        Returns:
            Dictionary with 'text' (if LLM response), 'function_calls' (if functions were called),
            and 'response_content' (the full response object for conversation history)
        """
        try:
            logger.info(f"Generating content with function calling, model: {self.model}")
            logger.debug(f"System prompt length: {len(system_prompt)}, User prompt length: {len(user_prompt) if user_prompt else 0}")
            logger.debug(f"Number of tools available: {len(tools)}")
            
            # Build contents list
            contents = []
            
            # Add conversation history if provided (includes previous model responses and function results)
            if conversation_history:
                contents.extend(conversation_history)
            
            # Add user prompt (only on first iteration)
            # Convert to Content object if it's a string
            if user_prompt:
                if isinstance(user_prompt, str):
                    # Create a Content object for the user message
                    user_content = types.Content(
                        role="user",
                        parts=[types.Part.from_text(user_prompt)]
                    )
                    contents.append(user_content)
                else:
                    # Already a Content object
                    contents.append(user_prompt)
            
            # Convert tools to Gemini format (only send on first iteration)
            gemini_tools = []
            if send_tools:
                for tool in tools:
                    gemini_tools.append(
                        types.Tool(
                            function_declarations=[
                                types.FunctionDeclaration(
                                    name=tool["name"],
                                    description=tool["description"],
                                    parameters=tool["parameters"]
                                )
                            ]
                        )
                    )
            
            response = self.client.models.generate_content(
                model=self.model,
                config=types.GenerateContentConfig(
                    system_instruction=system_prompt,
                    temperature=temperature,
                    tools=gemini_tools if gemini_tools else None,
                ),
                contents=contents,
            )

            if not response:
                logger.error("Invalid response from Gemini API: empty response")
                raise ValueError("Invalid response from Gemini API: empty response")

            # Check for function calls
            function_calls = []
            text_content = None
            
            if hasattr(response, 'candidates') and response.candidates:
                candidate = response.candidates[0]
                if hasattr(candidate, 'content') and candidate.content:
                    if hasattr(candidate.content, 'parts'):
                        for part in candidate.content.parts:
                            if hasattr(part, 'function_call'):
                                # Function call detected
                                func_call = part.function_call
                                # Convert function call args to dict
                                args_dict = {}
                                if hasattr(func_call, 'args'):
                                    # args is typically a dict-like object
                                    args_dict = dict(func_call.args) if func_call.args else {}
                                
                                function_calls.append({
                                    "name": func_call.name,
                                    "args": args_dict
                                })
                                logger.info(f"Function call detected: {func_call.name} with args: {list(args_dict.keys())}")
                            elif hasattr(part, 'text'):
                                # Text response
                                text_content = part.text
                                logger.info("Text response received from LLM")
            
            # Get the full response content for conversation history
            response_content = None
            if hasattr(response, 'candidates') and response.candidates:
                candidate = response.candidates[0]
                if hasattr(candidate, 'content') and candidate.content:
                    response_content = candidate.content
            
            result = {
                "model": self.model,
                "text": text_content,
                "function_calls": function_calls if function_calls else None,
                "response_content": response_content,  # Store for conversation history
            }
            
            if function_calls:
                logger.info(f"Function calling completed: {len(function_calls)} function(s) called")
            else:
                logger.info("Content generated successfully by Gemini (no function calls)")
            
            return result
        except Exception as e:
            logger.error(f"Error generating content with function calling: {e}", exc_info=True)
            raise

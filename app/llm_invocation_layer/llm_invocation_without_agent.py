from google.genai import types, Client
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from tools import SummarizePDFTool, SummarizeTextTool, DetectLanguageTool, ExtractPDFTextTool, FetchExchangeRateTool, FetchWeatherTool, EvaluateLLMResponsesTool, HallucinationCheckerTool
from tool_orchestrator_prompt import SYSTEM_PROMPT


client = Client()

response = client.models.generate_content(
    model='gemini-2.5-flash',

    contents='What is the weather like in Boston?',
    config=types.GenerateContentConfig(
        system_instruction=SYSTEM_PROMPT,
        temperature=0.0,
        tools=[SummarizePDFTool(), 
               SummarizeTextTool(), 
               DetectLanguageTool(), 
               ExtractPDFTextTool(), 
               FetchExchangeRateTool(), 
               FetchWeatherTool(), 
               EvaluateLLMResponsesTool(), 
               HallucinationCheckerTool()],
    ),
)

print(response.text)    
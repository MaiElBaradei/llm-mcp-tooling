# app/agents/gemini_agent.py
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.agents import create_agent
from dotenv import load_dotenv
from .llm_invocation_prompt import SYSTEM_PROMPT

from .tool_wrappers import (
    extract_pdf_tool,
    summarize_text_tool,
    summarize_pdf_tool,
    detect_language_tool,
    evaluate_llm_responses_tool,
    hallucination_checker_tool,
    fetch_weather_tool,
    fetch_exchange_rate_tool
)
 
# Load environment variables
load_dotenv()
class Agent():
    def __init__(self):
        # Initialize the Gemini model
        self.llm = ChatGoogleGenerativeAI(
            model="gemini-2.5-flash",
            temperature=0
        )

        # Define available tools
        self.tools = [
            extract_pdf_tool,
            summarize_text_tool,
            summarize_pdf_tool,
            detect_language_tool,
            fetch_weather_tool,
            fetch_exchange_rate_tool,
            evaluate_llm_responses_tool,
            hallucination_checker_tool
        ]

    def create_agent(self):
        # Create the agent using the modern create_agent API
        agent = create_agent(
            model=self.llm,
            tools=self.tools,
            system_prompt=SYSTEM_PROMPT,
        )
        return agent

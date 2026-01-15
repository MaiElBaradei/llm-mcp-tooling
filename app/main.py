import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from logging_config import configure_logging
from app.llm_invocation_layer.invoke_llm import invoke_llm
import asyncio

async def main() -> None:
	configure_logging()

	query = input("Enter your query: ")
	await invoke_llm(query)



if __name__ == "__main__":
	asyncio.run(main())
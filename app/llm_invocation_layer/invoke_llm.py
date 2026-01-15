from .llm_invocation_with_agent import Agent

async def invoke_llm(query: str) -> None:
	agent = Agent().create_agent()
	
	try:
		for chunk in agent.stream(  
			{"messages": [{"role": "user", "content": query}]},
			stream_mode="values",
		):
			if "messages" in chunk and chunk["messages"]:
				last_msg = chunk["messages"][-1]
				if hasattr(last_msg, "content"):
					print(last_msg.content)
				elif hasattr(last_msg, "tool_calls") and last_msg.tool_calls:
					print(f"Calling tools: {[tc['name'] for tc in last_msg.tool_calls]}")
	except Exception as e:
		print(f"Error during streaming: {e}")
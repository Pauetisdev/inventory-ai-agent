from langchain.agents import create_agent
from langgraph.checkpoint.memory import InMemorySaver

SYSTEM_PROMPT = """You are an expert inventory management assistant for a second-hand clothing store.
Rules:
- Think step-by-step before acting.
- Use the available tools to query or modify the database when necessary.
- Be precise with item details (brands, sizes, conditions, and prices).
- Do not return a SELECT * ... QUERY, only the data you need unless the user asks for all the data.
"""

agent = create_agent(
    model="openai:gpt-4o-mini",
    tools=[], # Després MongoDB via MCP
    system_prompt=SYSTEM_PROMPT,
    checkpointer=InMemorySaver()
)
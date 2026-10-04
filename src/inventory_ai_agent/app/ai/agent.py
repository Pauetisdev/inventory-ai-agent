from langchain.agents import create_agent
from langgraph.checkpoint.memory import InMemorySaver
from inventory_ai_agent.app.ai.tools import search_inventory, sell_clothing_item, add_clothing_item
from langchain.agents.middleware import HumanInTheLoopMiddleware

SYSTEM_PROMPT = """You are the personal backend inventory manager for my resale clothing business.
Rules:
- Think step-by-step before acting.
- Use the available tools to query, add, or delete items from the MongoDB database.
- Be precise with item details (brands, sizes, conditions, and prices).
- If I ask you to add an item but I don't provide all the necessary fields (name, category, brand, size, condition, price), ask me for the missing details before using the tool.
- Do not make up data if you don't know it.
- Keep responses short, technical, and direct. I am the owner, not a retail customer.
"""

tools = [search_inventory, sell_clothing_item, add_clothing_item]

agent = create_agent(
    model="openai:gpt-4o-mini",
    tools = tools,
    system_prompt=SYSTEM_PROMPT,
    checkpointer=InMemorySaver(),
    middleware=[
        HumanInTheLoopMiddleware(
            interrupt_on={"sell_clothing_item": {"allowed_decisions": ["approve", "reject"]}},
        ),
    ],
)
from langchain.agents import create_agent
from langchain.agents.structured_output import ResponseFormat
from langgraph.checkpoint.memory import InMemorySaver
from inventory_ai_agent.app.ai.tools import search_inventory, sell_clothing_item, add_clothing_item, update_clothing_item
from langchain.agents.middleware import HumanInTheLoopMiddleware
from inventory_ai_agent.app.models.requests import AgentResponse

SYSTEM_PROMPT = """You are the personal backend inventory manager for my resale clothing business.
Rules:
- Think step-by-step before acting.
- Use the available tools to query, add, or delete items from the MongoDB database.
- Be precise with item details (brands, sizes, conditions, and prices).
- If I ask you to add an item but I don't provide all the necessary fields (name, category, brand, size, condition, price), ask me for the missing details before using the tool.
- Do not make up data if you don't know it.
- Keep responses short, technical, and direct. I am the owner, not a retail customer.
NEVER ask for confirmation if you have enough information to deduce the item attributes (name, price, condition, brand, size, category). If the user provides an item to add, execute the `add_clothing_item` tool immediately. Do not list items back asking "is this correct?".
FORMATTING RULE FOR SEARCHES:
- When the user asks to see or search for items, ALWAYS format each item as a Python-like class constructor call, exactly like this:
- Item(id="...", name="...", brand="...", size="...", condition="...", price=...)
- Do not use Markdown tables. Use plain text with this class-like structure for each item.
"""

tools = [search_inventory, sell_clothing_item, add_clothing_item, update_clothing_item]

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
    response_format= AgentResponse
)
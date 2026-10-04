from langchain_core.tools import tool
from typing import Optional
from inventory_ai_agent.app.db import clothes_collection

@tool(parse_docstring=True)
async def search_inventory(category: Optional[str] = None) ->str:
    """Search for clothing items in the second-hand store inventory.

    Args:
        category (str, optional): The category to filter items by 
            (e.g., Samarreta, Pantaló, Abric, Sabates, Accessori). Defaults to None.

    Returns:
        str: A string containing the list of matching clothing items 
            found in the database, or a message if no items match.
    """

    query = {}
    if category:
        query['category'] = category

    items = []
    async for document in clothes_collection.find(query):
        document["_id"] = str(document["_id"])
        items.append(document)

    if not items:
        return "No s'ha trobat cap peça de roba a l'inventari amb aquests criteris."

    return str(items)
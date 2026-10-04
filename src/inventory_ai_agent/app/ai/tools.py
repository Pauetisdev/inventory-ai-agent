from langchain_core.tools import tool
from typing import Optional
from inventory_ai_agent.app.config.db import clothes_collection
from bson import ObjectId #tipus de dada especific de Mongo
from inventory_ai_agent.app.models.stock import ClothingItem

from typing import Optional

@tool(parse_docstring=True)
async def search_inventory(
    name: Optional[str] = None,
    category: Optional[str] = None,
    brand: Optional[str] = None,
    size: Optional[str] = None,
    condition: Optional[str] = None,
    price: Optional[float] = None
) -> str:
    """Search for items in your resale inventory.

    Args:
        name (str, optional): The specific name or title of the item.
        category (str, optional): The category of the item (e.g., T-Shirt, Trousers, Coat, Shoes, Accessory).
        brand (str, optional): The brand of the item (e.g., Nike, Asics).
        size (str, optional): The size of the item.
        condition (str, optional): The physical condition of the item.
        price (float, optional): The exact price of the item saved in the database.
    """
    query = {}
    if name:
        query['name'] = {"$regex": name, "$options": "i"}
    if category:
        query['category'] = category
        
    if brand:
        query['brand'] = {"$regex": brand, "$options": "i"}
    if size:
        query['size'] = size
    if condition:
        query['condition'] = condition
    if price is not None:
        query['price'] = price

    items = []
    async for document in clothes_collection.find(query):
        document["_id"] = str(document["_id"])
        items.append(document)

    if not items:
        return "No s'ha trobat cap peça a l'inventari."

    return str(items)

@tool(parse_docstring=True)
async def add_clothing_item(item: ClothingItem) -> str:
    """Add a newly acquired or purchased clothing item to the store's database inventory.
    
    Use this tool ONLY when the user explicitly wants to add, insert, or register a new piece of clothing to the stock.
    Do NOT use this tool to update or modify existing items.
    
    CRITICAL RULE: If the user's prompt is missing required information to create the item (such as category, brand, size, condition, or price), you MUST ask the user to provide the missing details BEFORE executing this tool. Do not guess, assume, or invent values for sizes, prices, or conditions.

    Args:
        item (ClothingItemCreate): A structured model containing all the required details of the clothing item.
    """
    try:
        item_dict = item.model_dump()
        
        result = await clothes_collection.insert_one(item_dict)
        return f"Successfully added new item to inventory with ID: {str(result.inserted_id)}"
        
    except Exception as e:
        return f"Error adding item: {str(e)}"


@tool(parse_docstring=True)
async def sell_clothing_item(item_id : str) -> str:
    """
    Sell or remove a clothing item from the inventory using its ID.

    Args:
        item_id (str): The unique MongoDB ID of the clothing item to remove.

    Returns:
        str: Confirmation message or error if not found.
    """

    try:
        obj_id = ObjectId(item_id)
        result = await clothes_collection.delete_one({"_id": obj_id})
        
        if result.deleted_count > 0:
            return f"Item with ID {item_id} has been successfully sold and removed from inventory."
        
        return "No clothing item was found with this ID."
    except Exception:
        return "Invalid ID format provided."
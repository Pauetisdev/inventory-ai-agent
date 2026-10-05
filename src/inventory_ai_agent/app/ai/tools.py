from langchain_core.tools import tool
from inventory_ai_agent.app.config.db import clothes_collection
from bson import ObjectId #tipus de dada especific de Mongo
from inventory_ai_agent.app.models.stock import ClothingItem

@tool(parse_docstring=True)
async def search_inventory(
    name: str | None = None,
    category: str | None = None,
    brand: str | None = None,
    size: str | None = None,
    condition: str | None = None,
    price: float | None = None
) -> str:
    """Searches for clothing items in the inventory. 
    CRITICAL: If the user wants to see all items or general stock, call this tool with NO arguments (all parameters as None) to retrieve the complete inventory list.

    Args:
        name (str, optional): Filter by item name.
        category (str, optional): Filter by category.
        brand (str, optional): Filter by brand.
        size (str, optional): Filter by size.
        condition (str, optional): Filter by condition.
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
    
    CRITICAL RULE: If the user's prompt is missing required information to create the item (such as category, brand, size, condition, or price),
        you MUST ask the user to provide the missing details BEFORE executing this tool. Do not guess, assume, or invent values for sizes, prices, or conditions.

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
async def sell_clothing_item(item_id: str) -> str:
    """Sell or remove a clothing item from the inventory using its unique ID.
    
    CRITICAL RULE: If the user asks to sell/remove an item by its name (e.g., "I sold the Nike shoes"), 
    you MUST first use the 'search_inventory' tool to find the item and retrieve its exact '_id'. 
    If multiple items match the name, ask the user to clarify which one they sold before proceeding.
    Do NOT guess the ID.

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

@tool(parse_docstring=True)
async def update_clothing_item(
    item_id: str,
    price: float | None = None,
    condition: str | None = None,
    name: str | None = None
) -> str:
    """Updates specific fields of an existing item in the resale inventory database.
    
    CRITICAL RULE: You MUST know the exact MongoDB 'item_id' to use this tool. 
    If the user asks to update an item but you don't know its ID, you must call 'search_inventory' first to retrieve the correct '_id'.

    Args:
        item_id (str): The unique MongoDB ObjectId of the item to update.
        price (float, optional): The purchase price (cost of acquisition) of the item.
        condition (str, optional): The updated physical condition of the item.
        name (str, optional): The updated specific name or title of the item.

    Returns:
        str: A message indicating the success or failure of the update operation in the database.
    """
    update_data = {}
    if price is not None:
        update_data["price"] = price
    if condition:
        update_data["condition"] = condition
    if name:
        update_data["name"] = name

    if not update_data:
        return "There are no data to update."

    try:
        result = await clothes_collection.update_one(
            {"_id": ObjectId(item_id)},
            {"$set": update_data}
        )
        
        if result.modified_count > 0:
            return f"Item {item_id} have updated correctly."
        else:
            return f"No changes have been made. The id {item_id} may not exist or the data may be identical to the current one."
    except Exception as e:
        return f"Database error updating item: {str(e)}"
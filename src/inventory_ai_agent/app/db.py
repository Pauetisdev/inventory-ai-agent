from motor.motor_asyncio import AsyncIOMotorClient
from inventory_ai_agent.app.core import settings

client = AsyncIOMotorClient(settings.mongo_uri)
db = client.get_database("inventory_db")

clothes_collection = db.get_collection("clothes")
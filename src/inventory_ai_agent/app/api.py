from fastapi import APIRouter, HTTPException
from typing import List
from pydantic import BaseModel, Field
from fastapi import HTTPException
from inventory_ai_agent.app.agent import agent
from langchain_core.runnables import RunnableConfig
from inventory_ai_agent.app.db import clothes_collection
from inventory_ai_agent.app.models.clothing import ClothingItemCreate, ClothingItemResponse


inventory_router = APIRouter(prefix="/inventory", tags=["Inventory"])

@inventory_router.post("/clothes", response_model=ClothingItemResponse, status_code=201)
async def create_clothing(item: ClothingItemCreate):
    # un cop validat passar a dict
    item_dict = item.model_dump()
    
    # Guardem a MongoDB
    result = await clothes_collection.insert_one(item_dict)
    
    created_item = await clothes_collection.find_one({"_id": result.inserted_id})
    if created_item:
        created_item["_id"] = str(created_item["_id"]) 
        return created_item # tornem el dict amb id pasat a str
        
    raise HTTPException(status_code=500, detail="Error al crear l'article")

@inventory_router.get("/clothes", response_model=List[ClothingItemResponse])
async def get_all_clothes():
    clothes = []

    async for document in clothes_collection.find({}):
        document["_id"] = str(document["_id"])
        clothes.append(document)
    return clothes


agent_router = APIRouter(prefix="/agent", tags=["AI Agent"])

class ChatRequest(BaseModel):
    message: str = Field(..., description="The user prompt or command for the inventory agent")
    thread_id: str = Field(default="default_thread", description="Unique thread identifier for conversation memory")

@agent_router.post("/chat")
async def chat_with_agent(payload: ChatRequest):
    try:
        
        config: RunnableConfig = {"configurable": {"thread_id": payload.thread_id}}
        
        response = agent.invoke(
            {"messages": [{"role": "user", "content": payload.message}]},
            config=config
        )
        
        ai_message = response["messages"][-1].content
        return {
            "thread_id": payload.thread_id,
            "response": ai_message
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
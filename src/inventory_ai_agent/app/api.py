from fastapi import APIRouter, HTTPException
from typing import List
from pydantic import BaseModel, Field
from fastapi import HTTPException
from inventory_ai_agent.app.ai.agent import agent
from langchain_core.runnables import RunnableConfig
from inventory_ai_agent.app.config.db import clothes_collection
from inventory_ai_agent.app.models.stock import ClothingItem
from inventory_ai_agent.app.models.requests import ChatRequest, ApproveRequest


agent_router = APIRouter(prefix="/agent", tags=["AI Agent"])


@agent_router.post("/chat")
async def chat_with_agent(payload: ChatRequest):
    try:
        config: RunnableConfig = {"configurable": {"thread_id": payload.thread_id}}
        
        # crida async
        response = await agent.ainvoke(
            {"messages": [{"role": "user", "content": payload.message}]},
            config=config
        )
        
        state = await agent.aget_state(config)

        # Comprovar que l'execució està pausada.
        if state.next:
            return {
                "thread_id": payload.thread_id,
                "status": "pending_human_approval",
                "message": "The agent has stopped. Manual approval is required to sell/remove the item.",
                "pending_action": state.next[0] # Aquí ens dirà quina eina està bloquejada
            }

        ai_message = response["messages"][-1].content
        return {
            "thread_id": payload.thread_id,
            "status": "completed",
            "response": ai_message
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@agent_router.post("/approve")
async def approve_agent_action(payload: ApproveRequest):
    try:
        config: RunnableConfig = {"configurable": {"thread_id": payload.thread_id}}
        
        state = await agent.aget_state(config)
        if not state.next:
            raise HTTPException(
                status_code=400, 
                detail="Aquest fil no té cap acció pendent d'aprovació."
            )
            
        response = await agent.ainvoke(
            {"messages": [{"role": "user", "content": payload.decision}]},
            config=config
        )
        
        ai_message = response["messages"][-1].content
        return {
            "thread_id": payload.thread_id,
            "status": "completed",
            "response": ai_message
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
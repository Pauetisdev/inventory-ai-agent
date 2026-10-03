from fastapi import APIRouter
from pydantic import BaseModel, Field
from fastapi import HTTPException
from inventory_ai_agent.app.agent import agent
from langchain_core.runnables import RunnableConfig

router = APIRouter(prefix="/agent", tags=["AI Agent"])

class ChatRequest(BaseModel):
    message: str = Field(..., description="The user prompt or command for the inventory agent")
    thread_id: str = Field(default="default_thread", description="Unique thread identifier for conversation memory")

@router.post("/chat")
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
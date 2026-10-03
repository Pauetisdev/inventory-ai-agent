from fastapi import FastAPI
import inventory_ai_agent.app.core
from inventory_ai_agent.app.api import router as agent_router

app = FastAPI(
    title="Inventory AI Agent",
    description="An AI agent that helps you manage your inventory",
    version="1.0.0",
)

app.include_router(agent_router)

@app.get("/")
async def health_check():
    return {
        "status": "ok",
        "message": "Server is running properly. Ready to receive the Agent!"
    }
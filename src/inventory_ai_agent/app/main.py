from fastapi import FastAPI

app = FastAPI(
    title="Inventory AI Agent",
    description="An AI agent that helps you manage your inventory",
    version="1.0.0",
)

@app.get("/")
async def health_check():
    return {
        "status": "ok",
        "message": "Server is running properly. Ready to receive the Agent!"
    }
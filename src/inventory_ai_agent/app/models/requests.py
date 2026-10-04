from pydantic import BaseModel, Field

class ChatRequest(BaseModel):
    message: str = Field(..., description="The user prompt or command for the inventory agent")
    thread_id: str = Field(default="default_thread", description="Unique thread identifier for conversation memory")

class ApproveRequest(BaseModel):
    thread_id: str = Field(..., description="The ID of the conversation thread that is paused")
    decision: str = Field(..., description="The human decision: 'approve' to confirm, 'reject' to cancel.")
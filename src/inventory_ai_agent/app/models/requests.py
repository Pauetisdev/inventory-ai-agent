from pydantic import BaseModel, Field

class ChatRequest(BaseModel):
    message: str = Field(..., description="The user prompt or command for the inventory agent")
    thread_id: str = Field(default="default_thread", description="Unique thread identifier for conversation memory")

class ApproveRequest(BaseModel):
    thread_id: str = Field(..., description="The ID of the conversation thread that is paused")
    decision: str = Field(..., description="The human decision: 'approve' to confirm, 'reject' to cancel.")

class AgentResponse(BaseModel):
    reply: str = Field(description="The natural language response to the user.")
    action_taken: str = Field(description="Summary of the action taken (e.g., 'item_added', 'search_completed', 'waiting_for_approval', 'item_deleted').")
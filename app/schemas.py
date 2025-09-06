from pydantic import BaseModel, Field

class ChatRequest(BaseModel):
    user_id: str = Field(..., min_length=1)
    message: str = Field(..., min_length=1)

class ChatResponse(BaseModel):
    reply: str
    model: str
    provider: str
    tokens_estimate: int | None = None

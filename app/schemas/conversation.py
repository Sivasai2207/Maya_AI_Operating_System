from datetime import datetime

from pydantic import BaseModel, ConfigDict


class ConversationCreate(BaseModel):
    title: str = "New Conversation"


class ConversationResponse(BaseModel):
    id: int
    title: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
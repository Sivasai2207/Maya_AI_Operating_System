from datetime import datetime

from pydantic import BaseModel, ConfigDict

from app.schemas.message import MessageResponse


class ConversationCreate(BaseModel):
    title: str = "New Conversation"


class ConversationResponse(BaseModel):
    id: int
    title: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class ConversationDetailResponse(BaseModel):
    id: int
    title: str
    created_at: datetime
    messages: list[MessageResponse]

    model_config = ConfigDict(from_attributes=True)
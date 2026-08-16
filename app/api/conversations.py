from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.models.conversation import Conversation
from app.models.message import Message
from app.schemas.conversation import (
    ConversationCreate,
    ConversationResponse,
)
from app.schemas.message import MessageCreate, MessageResponse


router = APIRouter(
    prefix="/conversations",
    tags=["Conversations"],
)


@router.post(
    "",
    response_model=ConversationResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_conversation(
    payload: ConversationCreate,
    db: Session = Depends(get_db),
):
    conversation = Conversation(title=payload.title)

    db.add(conversation)
    db.commit()
    db.refresh(conversation)

    return conversation


@router.post(
    "/{conversation_id}/messages",
    response_model=MessageResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_message(
    conversation_id: int,
    payload: MessageCreate,
    db: Session = Depends(get_db),
):
    conversation = db.get(Conversation, conversation_id)

    if conversation is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Conversation not found",
        )

    message = Message(
        conversation_id=conversation_id,
        role=payload.role,
        content=payload.content,
    )

    db.add(message)
    db.commit()
    db.refresh(message)

    return message
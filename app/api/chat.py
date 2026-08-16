from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import select


from app.core.prompts import MAYA_SYSTEM_PROMPT
from app.llm.nvidia import generate_response
from app.database.session import get_db
from app.models.conversation import Conversation
from app.models.message import Message
from app.schemas.chat import ChatRequest, ChatResponse
from app.services.memory_service import (get_memories,process_memory,)

router = APIRouter(
    prefix="/chat",
    tags=["Chat"],
)


@router.post(
    "",
    response_model=ChatResponse,
    status_code=status.HTTP_200_OK,
)
def chat(
    payload: ChatRequest,
    db: Session = Depends(get_db),
):
    # 1. Create a conversation automatically if one wasn't supplied.
    if payload.conversation_id is None:
        conversation = Conversation(title="New Conversation")
        db.add(conversation)
        db.commit()
        db.refresh(conversation)

    else:
        conversation = db.get(
            Conversation,
            payload.conversation_id,
        )

        if conversation is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Conversation not found",
            )

    # 2. Store the user's message.
    user_message = Message(
        conversation_id=conversation.id,
        role="user",
        content=payload.message,
    )

    db.add(user_message)
    db.commit()
    process_memory(
        db=db,
        user_message=payload.message,
    )
    # 3. Temporary Maya response.
    history = db.scalars(
        select(Message)
        .where(Message.conversation_id == conversation.id)
        .order_by(Message.created_at)
    ).all()
    memories = get_memories(db)
    memory_context = "\n".join(
    f"- {memory.content}"
    for memory in memories
)
    llm_messages = [
        {
            "role": "system",
            "content": f"""
            {MAYA_SYSTEM_PROMPT}
            Long-term memory about the user:
            {memory_context if memory_context else "No stored memories yet."}
            Use these memories only when relevant to the user's request.
            """,
        }
    ]
    for message in history:
        llm_messages.append(
            {
            "role": message.role,
            "content": message.content,
            }
        )
    maya_response = generate_response(llm_messages)

    # 4. Store Maya's response.
    assistant_message = Message(
        conversation_id=conversation.id,
        role="assistant",
        content=maya_response,
    )

    db.add(assistant_message)
    db.commit()

    return ChatResponse(
        conversation_id=conversation.id,
        user_message=payload.message,
        assistant_message=maya_response,
    )
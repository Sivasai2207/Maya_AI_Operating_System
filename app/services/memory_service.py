import json

from openai import OpenAI
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.config import settings
from app.models.memory import Memory


client = OpenAI(
    api_key=settings.nvidia_api_key,
    base_url=settings.nvidia_base_url,
)


MEMORY_CLASSIFIER_PROMPT = """
You are the memory manager for Maya, a personal AI assistant.

Analyze the user's message and determine whether it contains
information worth remembering across future conversations.

Store durable information such as:
- user preferences
- interests
- personal goals
- projects
- work preferences
- commonly used technologies
- stable facts useful in future conversations

Do NOT store:
- greetings
- temporary statements
- casual conversation
- one-time requests
- questions
- information useful only for the current conversation

Return ONLY valid JSON.

Use exactly this format:

{
  "action": "store" | "ignore",
  "category": "preference" | "interest" | "project" | "goal" | "personal" | "work" | "other",
  "memory": "short standalone fact"
}

If the message should not be remembered:

{
  "action": "ignore",
  "category": "other",
  "memory": ""
}
"""


def classify_memory(user_message: str) -> dict:
    response = client.chat.completions.create(
        model=settings.llm_model,
        messages=[
            {
                "role": "system",
                "content": MEMORY_CLASSIFIER_PROMPT,
            },
            {
                "role": "user",
                "content": user_message,
            },
        ],
        temperature=0,
        max_tokens=200,
    )

    content = response.choices[0].message.content

    if not content:
        return {
            "action": "ignore",
            "category": "other",
            "memory": "",
        }

    try:
        return json.loads(content)
    except json.JSONDecodeError:
        return {
            "action": "ignore",
            "category": "other",
            "memory": "",
        }


def process_memory(
    db: Session,
    user_message: str,
) -> None:
    result = classify_memory(user_message)

    if result.get("action") != "store":
        return

    memory_text = result.get("memory", "").strip()

    if not memory_text:
        return

    existing = db.scalar(
        select(Memory).where(
            Memory.content == memory_text
        )
    )

    if existing:
        return

    memory = Memory(
        category=result.get("category", "other"),
        content=memory_text,
    )

    db.add(memory)
    db.commit()

def get_memories(db: Session) -> list[Memory]:
    return list(
        db.scalars(
            select(Memory)
            .order_by(Memory.updated_at.desc())
            .limit(50)
        ).all()
    )
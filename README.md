# Maya AI Operating System

> Project README (Current Progress)

<details>
<summary><strong>Phase 0 – Project Setup</strong></summary>

## Goal
Build a personal AI operating system named **Maya** with persistent memory.

### Architecture Vision

```text
Flutter App
     │
     ▼
 FastAPI Backend
     │
 ┌───┴─────────────┐
 │                 │
PostgreSQL      NVIDIA LLM
 │                 │
 └──────► Maya ◄───┘
```

### Stack

- Flutter
- FastAPI
- Python + uv
- PostgreSQL
- SQLAlchemy
- Alembic
- NVIDIA Build API

### Completed
- Project initialized with `uv`
- FastAPI server running
- Configuration using `.env`
- PostgreSQL configured
- Alembic migrations enabled

</details>

<details open>
<summary><strong>Phase 1 – Foundation (Completed)</strong></summary>

# High Level Flow

```text
                 Flutter
                    │
                    ▼
               POST /chat
                    │
            FastAPI Backend
                    │
      ┌─────────────┼─────────────┐
      │             │             │
      ▼             ▼             ▼
Conversation    Long-Term      Prompt
 History         Memory        Builder
(Postgres)      (Postgres)
      │             │
      └──────┬──────┘
             ▼
      NVIDIA Nemotron
             ▼
        Maya Response
```

## Database

```text
conversations
      │
      └── messages

memories
```

## Conversation Flow

```text
User
 │
 ▼
POST /chat
 │
 ▼
Store user message
 │
 ▼
Retrieve conversation history
 │
 ▼
Retrieve long-term memories
 │
 ▼
Build prompt
 │
 ▼
NVIDIA LLM
 │
 ▼
Store assistant response
 │
 ▼
Return response
```

## Automatic Memory Flow

```text
User Message
      │
      ▼
Memory Classifier
      │
 ┌────┴────┐
 │         │
Ignore   Store
           │
           ▼
      memories table
```

## Cross-Conversation Memory

```text
Conversation A
"I love building AI agents."

        │
        ▼
 Stored in memories
        │
        ▼

Conversation B
"What do I love building?"

        │
        ▼
Retrieve memories
        │
        ▼
LLM answers correctly
```

## APIs

- POST `/chat`
- POST `/conversations`
- GET `/conversations/{id}`
- POST `/conversations/{id}/messages`
- GET `/health`
- GET `/db-health`

## Components

- FastAPI
- SQLAlchemy
- Alembic
- PostgreSQL
- NVIDIA Build API
- Conversation Memory
- Long-Term Memory (V1)

## What Maya Can Do

- Maintain conversation history
- Automatically classify durable memories
- Store long-term memories
- Recall memories in new conversations
- Generate responses using NVIDIA models

## Future Phases

- Memory Update/Delete
- Embeddings
- Vector Search
- Reflection Memory
- Tool Calling
- Voice
- RAG
- Agent Planning

</details>

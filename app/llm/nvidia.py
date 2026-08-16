from openai import OpenAI

from app.core.config import settings


client = OpenAI(
    api_key=settings.nvidia_api_key,
    base_url=settings.nvidia_base_url,
)


def generate_response(messages: list[dict[str, str]]) -> str:
    response = client.chat.completions.create(
        model=settings.llm_model,
        messages=messages,
        temperature=0.7,
        max_tokens=1024,
    )

    content = response.choices[0].message.content

    if not content:
        return "I couldn't generate a response."

    return content
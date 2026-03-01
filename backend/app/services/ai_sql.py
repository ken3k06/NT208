from langchain_openai import ChatOpenAI

from app.core.config import get_settings

settings = get_settings()


def answer_question(question: str) -> tuple[str, str | None]:
    """
    MVP stub: trả lời định hướng bằng LLM.
    Giai đoạn sau thay bằng Text-to-SQL có guardrail (SELECT-only + schema allowlist).
    """
    if not settings.openai_api_key:
        return (
            "AI chưa được cấu hình OPENAI_API_KEY. Hiện tại endpoint chat đang ở chế độ skeleton.",
            None,
        )

    llm = ChatOpenAI(model=settings.openai_model, api_key=settings.openai_api_key, temperature=0)
    prompt = (
        "Bạn là trợ lý học vụ. Trả lời ngắn gọn bằng tiếng Việt dựa trên câu hỏi sau: "
        f"{question}"
    )
    resp = llm.invoke(prompt)
    return (resp.content if isinstance(resp.content, str) else str(resp.content), None)

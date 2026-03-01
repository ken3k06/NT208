from fastapi import APIRouter

from app.schemas.chat import ChatAnswer, ChatQuery
from app.services.ai_sql import answer_question

router = APIRouter()


@router.post("/query", response_model=ChatAnswer)
def chat_query(payload: ChatQuery) -> ChatAnswer:
    answer, sql_preview = answer_question(payload.question)
    return ChatAnswer(answer=answer, sql_preview=sql_preview)

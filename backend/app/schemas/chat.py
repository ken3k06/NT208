from pydantic import BaseModel, Field


class ChatQuery(BaseModel):
    question: str = Field(min_length=5, max_length=500)


class ChatAnswer(BaseModel):
    answer: str
    sql_preview: str | None = None

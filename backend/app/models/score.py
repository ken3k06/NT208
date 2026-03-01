from sqlalchemy import Float, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class Score(Base):
    __tablename__ = "scores"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    student_id: Mapped[int] = mapped_column(ForeignKey("students.id", ondelete="CASCADE"), index=True)
    semester: Mapped[str] = mapped_column(String(20), index=True)
    course_code: Mapped[str] = mapped_column(String(20), index=True)
    credits: Mapped[int] = mapped_column(Integer)
    total_score: Mapped[float] = mapped_column(Float)

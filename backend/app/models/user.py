from enum import Enum
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Boolean, Enum as SQLAlchemyEnum

from app.db.base import Base

class UserRole(str, Enum):
    ADMIN = "ADMIN"      # Dean / Ban Chủ nhiệm Khoa
    ADVISOR = "ADVISOR"  # Advisor / Cố vấn học tập (CVHT)

class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    email: Mapped[str] = mapped_column(String, unique=True, index=True, nullable=False)
    hashed_password: Mapped[str] = mapped_column(String, nullable=False)
    full_name: Mapped[str | None] = mapped_column(String, nullable=True)
    role: Mapped[UserRole] = mapped_column(SQLAlchemyEnum(UserRole), default=UserRole.ADVISOR, nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)

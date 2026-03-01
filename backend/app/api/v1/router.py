from fastapi import APIRouter

from app.api.v1.endpoints import chat, dashboard, health, students

api_router = APIRouter()
api_router.include_router(health.router, prefix="/health", tags=["health"])
api_router.include_router(students.router, prefix="/students", tags=["students"])
api_router.include_router(dashboard.router, prefix="/dashboard", tags=["dashboard"])
api_router.include_router(chat.router, prefix="/chat", tags=["chat"])

from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.v1.deps import get_current_user
from app.core.config import get_settings
from app.db.session import get_db
from app.models.user import User, UserRole
from app.schemas.auth import LoginRequest, TokenResponse, UserOut
from app.services.security import create_access_token, hash_password, verify_password

router = APIRouter()
settings = get_settings()


@router.post("/login", response_model=TokenResponse)
def login(payload: LoginRequest, db: Session = Depends(get_db)) -> TokenResponse:
    user = db.query(User).filter(User.email == payload.email, User.is_active.is_(True)).first()
    if not user or not verify_password(payload.password, user.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid email or password")

    token = create_access_token(
        subject=user.email,
        role=user.role.value,
        expires_delta=timedelta(minutes=settings.access_token_expire_minutes),
    )
    return TokenResponse(access_token=token, role=user.role.value)


@router.get("/me", response_model=UserOut)
def me(current_user: User = Depends(get_current_user)) -> UserOut:
    return UserOut(
        id=current_user.id,
        email=current_user.email,
        full_name=current_user.full_name,
        role=current_user.role.value,
    )


@router.post("/seed-users")
def seed_users(db: Session = Depends(get_db)) -> dict:
    seeds = [
        {"email": "admin@uit.edu.vn", "password": "admin123", "full_name": "Dean Admin", "role": UserRole.ADMIN},
        {
            "email": "advisor1@uit.edu.vn",
            "password": "advisor123",
            "full_name": "Advisor One",
            "role": UserRole.ADVISOR,
        },
    ]

    created = 0
    for item in seeds:
        existing = db.query(User).filter(User.email == item["email"]).first()
        if existing:
            continue
        user = User(
            email=item["email"],
            hashed_password=hash_password(item["password"]),
            full_name=item["full_name"],
            role=item["role"],
            is_active=True,
        )
        db.add(user)
        created += 1

    db.commit()
    return {"message": "Seed users completed", "created": created}

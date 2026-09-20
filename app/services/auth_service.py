from typing import Any
from fastapi import HTTPException, status
import jwt
from sqlalchemy.orm import Session

from app.core.security import (
    create_access_token,
    decode_access_token,
    hash_password,
    verify_hash
)
from app.models.user import User
from app.repositories.user import UserRepository
from app.schemas.user import UserCreate

def register(db: Session, data: UserCreate):
    user_repository = UserRepository(db)
    if user_repository.get_by_username(data.username):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already taken"
        )
    values = data.model_dump(exclude={"password"})
    values["hashed_password"] = hash_password(data.password)
    return user_repository.create(values)

def authenticate(db: Session, username: str, password: str):
    user_repository = UserRepository(db)
    user = user_repository.get_by_username(username)
    if not user or not verify_hash(password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"}
        )
    return {
        "access_token": create_access_token(user.id),
        "token_type": "bearer",
    }

def get_user_from_token(db: Session, token: str):
    credentials_error = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid or expired token",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload: dict[str, Any] = decode_access_token(token)
        subject = payload.get("sub")
        if not isinstance(subject, str) or not subject.strip():
            raise credentials_error
        user_id = int(subject)
        if user_id <= 0:
            raise credentials_error
    except Exception as e:
        raise credentials_error

    user_repository = UserRepository(db)
    user = user_repository.get_by_id(user_id)
    if user is None:
        raise credentials_error

    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Your account is inactive",
        )
    return user

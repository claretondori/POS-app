from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from passlib.context import CryptContext

from app.repositories.user import UserRepository
from app.schemas import user as schemas

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class UserService:
    def __init__(self, db: Session):
        self.repo = UserRepository(db)

    def list(self, skip: int = 0, limit: int = 100):
        return self.repo.get_all(skip, limit)

    def get(self, user_id: int):
        obj = self.repo.get(user_id)
        if not obj:
            raise HTTPException(status.HTTP_404_NOT_FOUND, "User not found")
        return obj

    def create(self, data: schemas.UserCreate):
        if self.repo.get_by_username(data.username):
            raise HTTPException(status.HTTP_400_BAD_REQUEST, "Username already taken")
        payload = data.model_dump(exclude={"password"})
        payload["password_hash"] = pwd_context.hash(data.password)
        return self.repo.create(payload)

    def update(self, user_id: int, data: schemas.UserUpdate):
        obj = self.get(user_id)
        payload = data.model_dump(exclude_unset=True, exclude={"password"})
        if data.password:
            payload["password_hash"] = pwd_context.hash(data.password)
        return self.repo.update(obj, payload)

    def delete(self, user_id: int):
        obj = self.get(user_id)
        self.repo.delete(obj)


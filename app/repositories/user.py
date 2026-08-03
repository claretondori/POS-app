import enum

from sqlalchemy.orm import relationship, Session

from app.models.user import User

class UserRole(str, enum.Enum):
    admin = "admin"
    manager = "manager"
    cashier = "cashier"





class UserRepository:
    def __init__(self, db: Session):
        self.db = db

    def get(self, user_id: int):
        return self.db.query(User).filter(User.user_id == user_id).first()

    def get_by_username(self, username: str):
        return self.db.query(User).filter(User.username == username).first()

    def get_all(self, skip: int = 0, limit: int = 100):
        return self.db.query(User).offset(skip).limit(limit).all()

    def create(self, data: dict):
        obj = User(**data)
        self.db.add(obj)
        self.db.commit()
        self.db.refresh(obj)
        return obj

    def update(self, obj: User, data: dict):
        for field, value in data.items():
            if value is not None:
                setattr(obj, field, value)
        self.db.commit()
        self.db.refresh(obj)
        return obj

    def delete(self, obj: User):
        self.db.delete(obj)
        self.db.commit()


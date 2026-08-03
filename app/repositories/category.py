from sqlalchemy.orm import relationship, Session
from app.models.category import Category


class CategoryRepository:
    def __init__(self, db: Session):
        self.db = db

    def get(self, category_id: int):
        return self.db.query(Category).filter(Category.category_id == category_id).first()

    def get_by_name(self, name: str):
        return self.db.query(Category).filter(Category.name == name).first()

    def get_all(self, skip: int = 0, limit: int = 100):
        return self.db.query(Category).offset(skip).limit(limit).all()

    def create(self, data: dict):
        obj = Category(**data)
        self.db.add(obj)
        self.db.commit()
        self.db.refresh(obj)
        return obj

    def update(self, obj: Category, data: dict):
        for field, value in data.items():
            if value is not None:
                setattr(obj, field, value)
        self.db.commit()
        self.db.refresh(obj)
        return obj

    def delete(self, obj: Category):
        self.db.delete(obj)
        self.db.commit()



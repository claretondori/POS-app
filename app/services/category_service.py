from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.repositories.category import CategoryRepository
from app.schemas import category as schemas


class CategoryService:
    def __init__(self, db: Session):
        self.repo = CategoryRepository(db)

    def list(self, skip: int = 0, limit: int = 100):
        return self.repo.get_all(skip, limit)

    def get(self, category_id: int):
        obj = self.repo.get(category_id)
        if not obj:
            raise HTTPException(status.HTTP_404_NOT_FOUND, "Category not found")
        return obj

    def create(self, data: schemas.CategoryCreate):
        if self.repo.get_by_name(data.name):
            raise HTTPException(status.HTTP_400_BAD_REQUEST, "Category name already exists")
        return self.repo.create(data.model_dump())

    def update(self, category_id: int, data: schemas.CategoryUpdate):
        obj = self.get(category_id)
        return self.repo.update(obj, data.model_dump(exclude_unset=True))

    def delete(self, category_id: int):
        obj = self.get(category_id)
        self.repo.delete(obj)


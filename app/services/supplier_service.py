from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.repositories.supplier import SupplierRepository
from app.schemas import supplier as schemas


class SupplierService:
    def __init__(self, db: Session):
        self.repo = SupplierRepository(db)

    def list(self, skip: int = 0, limit: int = 100):
        return self.repo.get_all(skip, limit)

    def get(self, supplier_id: int):
        obj = self.repo.get(supplier_id)
        if not obj:
            raise HTTPException(status.HTTP_404_NOT_FOUND, "Supplier not found")
        return obj

    def create(self, data: schemas.SupplierCreate):
        return self.repo.create(data.model_dump())

    def update(self, supplier_id: int, data: schemas.SupplierUpdate):
        obj = self.get(supplier_id)
        return self.repo.update(obj, data.model_dump(exclude_unset=True))

    def delete(self, supplier_id: int):
        obj = self.get(supplier_id)
        self.repo.delete(obj)


from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.repositories.product import ProductRepository
from app.repositories.category import CategoryRepository
from app.repositories.supplier import SupplierRepository
from app.schemas import product as schemas


class ProductService:
    def __init__(self, db: Session):
        self.repo = ProductRepository(db)
        self.category_repo = CategoryRepository(db)
        self.supplier_repo = SupplierRepository(db)

    def list(self, skip: int = 0, limit: int = 100):
        return self.repo.get_all(skip, limit)

    def low_stock(self):
        return self.repo.get_low_stock()

    def get(self, product_id: int):
        obj = self.repo.get(product_id)
        if not obj:
            raise HTTPException(status.HTTP_404_NOT_FOUND, "Product not found")
        return obj

    def create(self, data: schemas.ProductCreate):
        if self.repo.get_by_sku(data.sku):
            raise HTTPException(status.HTTP_400_BAD_REQUEST, "SKU already exists")
        if not self.category_repo.get(data.category_id):
            raise HTTPException(status.HTTP_400_BAD_REQUEST, "Category does not exist")
        if data.supplier_id and not self.supplier_repo.get(data.supplier_id):
            raise HTTPException(status.HTTP_400_BAD_REQUEST, "Supplier does not exist")
        return self.repo.create(data.model_dump())

    def update(self, product_id: int, data: schemas.ProductUpdate):
        obj = self.get(product_id)
        if data.category_id and not self.category_repo.get(data.category_id):
            raise HTTPException(status.HTTP_400_BAD_REQUEST, "Category does not exist")
        if data.supplier_id and not self.supplier_repo.get(data.supplier_id):
            raise HTTPException(status.HTTP_400_BAD_REQUEST, "Supplier does not exist")
        return self.repo.update(obj, data.model_dump(exclude_unset=True))

    def delete(self, product_id: int):
        obj = self.get(product_id)
        self.repo.delete(obj)


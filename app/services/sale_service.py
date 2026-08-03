from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.repositories.sale import SaleRepository, SaleStatus
from app.repositories.user import UserRepository
from app.repositories.customer import CustomerRepository
from app.schemas import sale as schemas


class SaleService:
    def __init__(self, db: Session):
        self.repo = SaleRepository(db)
        self.user_repo = UserRepository(db)
        self.customer_repo = CustomerRepository(db)

    def list(self, skip: int = 0, limit: int = 100):
        return self.repo.get_all(skip, limit)

    def get(self, sale_id: int):
        obj = self.repo.get(sale_id)
        if not obj:
            raise HTTPException(status.HTTP_404_NOT_FOUND, "Sale not found")
        return obj

    def create(self, data: schemas.SaleCreate):
        if not self.user_repo.get(data.user_id):
            raise HTTPException(status.HTTP_400_BAD_REQUEST, "User does not exist")
        if data.customer_id and not self.customer_repo.get(data.customer_id):
            raise HTTPException(status.HTTP_400_BAD_REQUEST, "Customer does not exist")
        return self.repo.create({
            "customer_id": data.customer_id,
            "user_id": data.user_id,
            "total_amount": 0,
            "status": SaleStatus.completed.value,
        })

    def update(self, sale_id: int, data: schemas.SaleUpdate):
        obj = self.get(sale_id)
        payload = data.model_dump(exclude_unset=True)
        if "status" in payload and payload["status"] is not None:
            payload["status"] = payload["status"].value if hasattr(payload["status"], "value") else payload["status"]
        return self.repo.update(obj, payload)

    def delete(self, sale_id: int):
        obj = self.get(sale_id)
        # restock any items before the cascade delete removes them
        for item in obj.sale_items:
            if item.product:
                item.product.quantity_in_stock += item.quantity
        self.repo.delete(obj)


import uuid

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.repositories.receipt import ReceiptRepository
from app.repositories.sale import SaleRepository
from app.repositories.user import UserRepository
from app.schemas import receipt as schemas


class ReceiptService:
    def __init__(self, db: Session):
        self.repo = ReceiptRepository(db)
        self.sale_repo = SaleRepository(db)
        self.user_repo = UserRepository(db)

    def list(self, skip: int = 0, limit: int = 100):
        return self.repo.get_all(skip, limit)

    def get(self, receipt_id: int):
        obj = self.repo.get(receipt_id)
        if not obj:
            raise HTTPException(status.HTTP_404_NOT_FOUND, "Receipt not found")
        return obj

    def get_for_sale(self, sale_id: int):
        obj = self.repo.get_by_sale(sale_id)
        if not obj:
            raise HTTPException(status.HTTP_404_NOT_FOUND, "No receipt for this sale yet")
        return obj

    def create(self, data: schemas.ReceiptCreate):
        sale = self.sale_repo.get(data.sale_id)
        if not sale:
            raise HTTPException(status.HTTP_400_BAD_REQUEST, "Sale does not exist")
        if self.repo.get_by_sale(data.sale_id):
            raise HTTPException(status.HTTP_400_BAD_REQUEST, "Receipt already exists for this sale")
        if not self.user_repo.get(data.issued_by):
            raise HTTPException(status.HTTP_400_BAD_REQUEST, "Issuing user does not exist")

        receipt_number = f"RCPT-{data.sale_id:06d}-{uuid.uuid4().hex[:6].upper()}"
        return self.repo.create({
            "sale_id": data.sale_id,
            "issued_by": data.issued_by,
            "receipt_number": receipt_number,
        })

    def update(self, receipt_id: int, data: schemas.ReceiptUpdate):
        obj = self.get(receipt_id)
        if data.issued_by is not None and not self.user_repo.get(data.issued_by):
            raise HTTPException(status.HTTP_400_BAD_REQUEST, "Issuing user does not exist")
        return self.repo.update(obj, data.model_dump(exclude_unset=True))

    def delete(self, receipt_id: int):
        obj = self.get(receipt_id)
        self.repo.delete(obj)


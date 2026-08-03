from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.repositories.payment import PaymentRepository
from app.repositories.sale import SaleRepository
from app.schemas import payment as schemas


class PaymentService:
    def __init__(self, db: Session):
        self.repo = PaymentRepository(db)
        self.sale_repo = SaleRepository(db)

    def list(self, skip: int = 0, limit: int = 100):
        return self.repo.get_all(skip, limit)

    def list_for_sale(self, sale_id: int):
        return self.repo.get_by_sale(sale_id)

    def get(self, payment_id: int):
        obj = self.repo.get(payment_id)
        if not obj:
            raise HTTPException(status.HTTP_404_NOT_FOUND, "Payment not found")
        return obj

    def _validate_amount(self, sale_id: int, amount, exclude_payment_id=None):
        sale = self.sale_repo.get(sale_id)
        if not sale:
            raise HTTPException(status.HTTP_400_BAD_REQUEST, "Sale does not exist")
        payments = self.repo.get_by_sale(sale_id)
        already_paid = sum(p.amount_paid for p in payments if p.payment_id != exclude_payment_id)
        if already_paid + amount > sale.total_amount:
            raise HTTPException(
                status.HTTP_400_BAD_REQUEST,
                f"Payment exceeds amount owed (owed {sale.total_amount - already_paid})",
            )

    def create(self, data: schemas.PaymentCreate):
        self._validate_amount(data.sale_id, data.amount_paid)
        payload = data.model_dump()
        payload["payment_method"] = data.payment_method.value
        return self.repo.create(payload)

    def update(self, payment_id: int, data: schemas.PaymentUpdate):
        obj = self.get(payment_id)
        if data.amount_paid is not None:
            self._validate_amount(obj.sale_id, data.amount_paid, exclude_payment_id=obj.payment_id)
        payload = data.model_dump(exclude_unset=True)
        if payload.get("payment_method") is not None:
            payload["payment_method"] = payload["payment_method"].value if hasattr(payload["payment_method"], "value") else payload["payment_method"]
        return self.repo.update(obj, payload)

    def delete(self, payment_id: int):
        obj = self.get(payment_id)
        self.repo.delete(obj)


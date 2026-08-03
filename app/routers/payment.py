from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.services.payment_service import PaymentService
from app.schemas import payment as schemas

router = APIRouter(prefix="/payments", tags=["Payments"])


@router.get("/", response_model=List[schemas.PaymentOut])
def list_payments(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return PaymentService(db).list(skip, limit)


@router.get("/by-sale/{sale_id}", response_model=List[schemas.PaymentOut])
def list_payments_for_sale(sale_id: int, db: Session = Depends(get_db)):
    return PaymentService(db).list_for_sale(sale_id)


@router.get("/{payment_id}", response_model=schemas.PaymentOut)
def get_payment(payment_id: int, db: Session = Depends(get_db)):
    return PaymentService(db).get(payment_id)


@router.post("/", response_model=schemas.PaymentOut, status_code=201)
def create_payment(data: schemas.PaymentCreate, db: Session = Depends(get_db)):
    return PaymentService(db).create(data)


@router.put("/{payment_id}", response_model=schemas.PaymentOut)
def update_payment(payment_id: int, data: schemas.PaymentUpdate, db: Session = Depends(get_db)):
    return PaymentService(db).update(payment_id, data)


@router.delete("/{payment_id}", status_code=204)
def delete_payment(payment_id: int, db: Session = Depends(get_db)):
    PaymentService(db).delete(payment_id)


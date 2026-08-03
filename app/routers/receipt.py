from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.services.receipt_service import ReceiptService
from app.schemas import receipt as schemas

router = APIRouter(prefix="/receipts", tags=["Receipts"])


@router.get("/", response_model=List[schemas.ReceiptOut])
def list_receipts(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return ReceiptService(db).list(skip, limit)


@router.get("/by-sale/{sale_id}", response_model=schemas.ReceiptOut)
def get_receipt_for_sale(sale_id: int, db: Session = Depends(get_db)):
    return ReceiptService(db).get_for_sale(sale_id)


@router.get("/{receipt_id}", response_model=schemas.ReceiptOut)
def get_receipt(receipt_id: int, db: Session = Depends(get_db)):
    return ReceiptService(db).get(receipt_id)


@router.post("/", response_model=schemas.ReceiptOut, status_code=201)
def create_receipt(data: schemas.ReceiptCreate, db: Session = Depends(get_db)):
    return ReceiptService(db).create(data)


@router.put("/{receipt_id}", response_model=schemas.ReceiptOut)
def update_receipt(receipt_id: int, data: schemas.ReceiptUpdate, db: Session = Depends(get_db)):
    return ReceiptService(db).update(receipt_id, data)


@router.delete("/{receipt_id}", status_code=204)
def delete_receipt(receipt_id: int, db: Session = Depends(get_db)):
    ReceiptService(db).delete(receipt_id)


from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.services.sale_service import SaleService
from app.schemas import sale as schemas

router = APIRouter(prefix="/sales", tags=["Sales"])


@router.get("/", response_model=List[schemas.SaleOut])
def list_sales(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return SaleService(db).list(skip, limit)


@router.get("/{sale_id}", response_model=schemas.SaleOut)
def get_sale(sale_id: int, db: Session = Depends(get_db)):
    return SaleService(db).get(sale_id)


@router.post("/", response_model=schemas.SaleOut, status_code=201)
def create_sale(data: schemas.SaleCreate, db: Session = Depends(get_db)):
    return SaleService(db).create(data)


@router.put("/{sale_id}", response_model=schemas.SaleOut)
def update_sale(sale_id: int, data: schemas.SaleUpdate, db: Session = Depends(get_db)):
    return SaleService(db).update(sale_id, data)


@router.delete("/{sale_id}", status_code=204)
def delete_sale(sale_id: int, db: Session = Depends(get_db)):
    SaleService(db).delete(sale_id)


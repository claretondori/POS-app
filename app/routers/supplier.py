from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.services.supplier_service import SupplierService
from app.schemas import supplier as schemas

router = APIRouter(prefix="/suppliers", tags=["Suppliers"])


@router.get("/", response_model=List[schemas.SupplierOut])
def list_suppliers(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return SupplierService(db).list(skip, limit)


@router.get("/{supplier_id}", response_model=schemas.SupplierOut)
def get_supplier(supplier_id: int, db: Session = Depends(get_db)):
    return SupplierService(db).get(supplier_id)


@router.post("/", response_model=schemas.SupplierOut, status_code=201)
def create_supplier(data: schemas.SupplierCreate, db: Session = Depends(get_db)):
    return SupplierService(db).create(data)


@router.put("/{supplier_id}", response_model=schemas.SupplierOut)
def update_supplier(supplier_id: int, data: schemas.SupplierUpdate, db: Session = Depends(get_db)):
    return SupplierService(db).update(supplier_id, data)


@router.delete("/{supplier_id}", status_code=204)
def delete_supplier(supplier_id: int, db: Session = Depends(get_db)):
    SupplierService(db).delete(supplier_id)


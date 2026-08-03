from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.services.sale_item_service import SaleItemService
from app.schemas import sale_item as schemas

router = APIRouter(prefix="/sale-items", tags=["Sale Items"])


@router.get("/", response_model=List[schemas.SaleItemOut])
def list_sale_items(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return SaleItemService(db).list(skip, limit)


@router.get("/by-sale/{sale_id}", response_model=List[schemas.SaleItemOut])
def list_items_for_sale(sale_id: int, db: Session = Depends(get_db)):
    return SaleItemService(db).list_for_sale(sale_id)


@router.get("/{sale_item_id}", response_model=schemas.SaleItemOut)
def get_sale_item(sale_item_id: int, db: Session = Depends(get_db)):
    return SaleItemService(db).get(sale_item_id)


@router.post("/", response_model=schemas.SaleItemOut, status_code=201)
def create_sale_item(data: schemas.SaleItemCreate, db: Session = Depends(get_db)):
    """Creates the line item, decrements product stock, and updates the sale total."""
    return SaleItemService(db).create(data)


@router.put("/{sale_item_id}", response_model=schemas.SaleItemOut)
def update_sale_item(sale_item_id: int, data: schemas.SaleItemUpdate, db: Session = Depends(get_db)):
    return SaleItemService(db).update(sale_item_id, data)


@router.delete("/{sale_item_id}", status_code=204)
def delete_sale_item(sale_item_id: int, db: Session = Depends(get_db)):
    SaleItemService(db).delete(sale_item_id)


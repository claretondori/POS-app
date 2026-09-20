from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.services.product_service import ProductService
from app.schemas import product as schemas
from app.dependencies import get_current_user
router = APIRouter(
    prefix="/products", 
    tags=["Products"], 
    dependencies= [Depends(get_current_user)],

    )


@router.get("/", response_model=List[schemas.ProductOut])
def list_products(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return ProductService(db).list(skip, limit)


@router.get("/low-stock", response_model=List[schemas.ProductOut])
def low_stock_products(db: Session = Depends(get_db)):
    return ProductService(db).low_stock()


@router.get("/{product_id}", response_model=schemas.ProductOut)
def get_product(product_id: int, db: Session = Depends(get_db)):
    return ProductService(db).get(product_id)


@router.post("/", response_model=schemas.ProductOut, status_code=201)
def create_product(data: schemas.ProductCreate, db: Session = Depends(get_db)):
    return ProductService(db).create(data)


@router.put("/{product_id}", response_model=schemas.ProductOut)
def update_product(product_id: int, data: schemas.ProductUpdate, db: Session = Depends(get_db)):
    return ProductService(db).update(product_id, data)


@router.delete("/{product_id}", status_code=204)
def delete_product(product_id: int, db: Session = Depends(get_db)):
    ProductService(db).delete(product_id)


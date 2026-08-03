from datetime import datetime
from decimal import Decimal
from typing import Optional
from pydantic import BaseModel, ConfigDict, Field


class ProductCreate(BaseModel):
    sku: str = Field(..., max_length=50)
    name: str = Field(..., max_length=150)
    category_id: int
    supplier_id: Optional[int] = None
    unit_price: Decimal = Field(..., ge=0)
    cost_price: Decimal = Field(..., ge=0)
    quantity_in_stock: int = Field(0, ge=0)
    reorder_level: Optional[int] = None


class ProductUpdate(BaseModel):
    sku: Optional[str] = None
    name: Optional[str] = None
    category_id: Optional[int] = None
    supplier_id: Optional[int] = None
    unit_price: Optional[Decimal] = None
    cost_price: Optional[Decimal] = None
    quantity_in_stock: Optional[int] = None
    reorder_level: Optional[int] = None


class ProductOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    product_id: int
    sku: str
    name: str
    category_id: int
    supplier_id: Optional[int]
    unit_price: Decimal
    cost_price: Decimal
    quantity_in_stock: int
    reorder_level: Optional[int]
    created_at: datetime


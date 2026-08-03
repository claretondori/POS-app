from decimal import Decimal
from typing import Optional
from pydantic import BaseModel, ConfigDict, Field


class SaleItemCreate(BaseModel):
    sale_id: int
    product_id: int
    quantity: int = Field(..., gt=0)


class SaleItemUpdate(BaseModel):
    quantity: Optional[int] = Field(None, gt=0)


class SaleItemOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    sale_item_id: int
    sale_id: int
    product_id: int
    quantity: int
    unit_price: Decimal
    subtotal: Decimal


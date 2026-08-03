from datetime import datetime
from decimal import Decimal
from typing import Optional
from pydantic import BaseModel, ConfigDict

from app.repositories.sale import SaleStatus


class SaleCreate(BaseModel):
    customer_id: Optional[int] = None
    user_id: int


class SaleUpdate(BaseModel):
    customer_id: Optional[int] = None
    status: Optional[SaleStatus] = None


class SaleOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    sale_id: int
    customer_id: Optional[int]
    user_id: int
    sale_date: datetime
    total_amount: Decimal
    status: str


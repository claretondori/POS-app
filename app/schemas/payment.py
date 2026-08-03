from datetime import datetime
from decimal import Decimal
from typing import Optional
from pydantic import BaseModel, ConfigDict, Field

from app.repositories.payment import PaymentMethod


class PaymentCreate(BaseModel):
    sale_id: int
    payment_method: PaymentMethod
    amount_paid: Decimal = Field(..., gt=0)
    transaction_reference: Optional[str] = None


class PaymentUpdate(BaseModel):
    payment_method: Optional[PaymentMethod] = None
    amount_paid: Optional[Decimal] = Field(None, gt=0)
    transaction_reference: Optional[str] = None


class PaymentOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    payment_id: int
    sale_id: int
    payment_method: str
    amount_paid: Decimal
    payment_date: datetime
    transaction_reference: Optional[str]


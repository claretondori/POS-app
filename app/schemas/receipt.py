from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict


class ReceiptCreate(BaseModel):
    sale_id: int
    issued_by: int


class ReceiptUpdate(BaseModel):
    issued_by: Optional[int] = None


class ReceiptOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    receipt_id: int
    sale_id: int
    issued_by: int
    receipt_number: str
    issued_date: datetime


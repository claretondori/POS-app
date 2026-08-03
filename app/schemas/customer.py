from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict, EmailStr, Field


class CustomerCreate(BaseModel):
    full_name: str = Field(..., max_length=100)
    phone: Optional[str] = None
    email: Optional[EmailStr] = None
    address: Optional[str] = None
    loyalty_points: int = 0


class CustomerUpdate(BaseModel):
    full_name: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[EmailStr] = None
    address: Optional[str] = None
    loyalty_points: Optional[int] = None


class CustomerOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    customer_id: int
    full_name: str
    phone: Optional[str]
    email: Optional[str]
    address: Optional[str]
    loyalty_points: int
    created_at: datetime


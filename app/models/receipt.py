import enum

from sqlalchemy import (
    Column, 
    Integer, 
    String, 
    Text, 
    DateTime,
    Numeric,
    Boolean, 
    ForeignKey, 
    Enum
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.database import Base


class UserRole(str, enum.Enum):
    admin = "admin"
    manager = "manager"
    cashier = "cashier"


class SaleStatus(str, enum.Enum):
    completed = "completed"
    voided = "voided"
    refunded = "refunded"


class PaymentMethod(str, enum.Enum):
    cash = "cash"
    card = "card"
    mobile_money = "mobile_money"

class Receipt(Base):
    __tablename__ = "receipts"

    receipt_id = Column(Integer, primary_key=True, index=True)
    sale_id = Column(Integer, ForeignKey("sales.sale_id"), nullable=False, unique=True)
    issued_by = Column(Integer, ForeignKey("users.user_id"), nullable=False)
    receipt_number = Column(String(50), nullable=False, unique=True)
    issued_date = Column(DateTime(timezone=True), server_default=func.now())

    sale = relationship("Sale", back_populates="receipt")
    issued_by_user = relationship("User", back_populates="receipts_issued")


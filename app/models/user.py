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

class User(Base):
    __tablename__ = "users"

    user_id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), nullable=False, unique=True, index=True)
    password_hash = Column(String(255), nullable=False)
    full_name = Column(String(100), nullable=False)
    role = Column(Enum(UserRole), nullable=False, default=UserRole.cashier)
    email = Column(String(100), nullable=True)
    is_active = Column(Boolean, nullable=False, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    sales = relationship("Sale", back_populates="user")
    receipts_issued = relationship("Receipt", back_populates="issued_by_user")

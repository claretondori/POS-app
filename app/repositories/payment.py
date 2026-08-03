import enum

from sqlalchemy.orm import relationship, Session

from app.models.payment import Payment

class PaymentMethod(str, enum.Enum):
    cash = "cash"
    card = "card"
    mobile_money = "mobile_money"





class PaymentRepository:
    def __init__(self, db: Session):
        self.db = db

    def get(self, payment_id: int):
        return self.db.query(Payment).filter(Payment.payment_id == payment_id).first()

    def get_by_sale(self, sale_id: int):
        return self.db.query(Payment).filter(Payment.sale_id == sale_id).all()

    def get_all(self, skip: int = 0, limit: int = 100):
        return self.db.query(Payment).offset(skip).limit(limit).all()

    def create(self, data: dict):
        obj = Payment(**data)
        self.db.add(obj)
        self.db.commit()
        self.db.refresh(obj)
        return obj

    def update(self, obj: Payment, data: dict):
        for field, value in data.items():
            if value is not None:
                setattr(obj, field, value)
        self.db.commit()
        self.db.refresh(obj)
        return obj

    def delete(self, obj: Payment):
        self.db.delete(obj)
        self.db.commit()


from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship, Session
from sqlalchemy.sql import func

from app.models.receipt import Receipt


class ReceiptRepository:
    def __init__(self, db: Session):
        self.db = db

    def get(self, receipt_id: int):
        return self.db.query(Receipt).filter(Receipt.receipt_id == receipt_id).first()

    def get_by_sale(self, sale_id: int):
        return self.db.query(Receipt).filter(Receipt.sale_id == sale_id).first()

    def get_all(self, skip: int = 0, limit: int = 100):
        return self.db.query(Receipt).offset(skip).limit(limit).all()

    def create(self, data: dict):
        obj = Receipt(**data)
        self.db.add(obj)
        self.db.commit()
        self.db.refresh(obj)
        return obj

    def update(self, obj: Receipt, data: dict):
        for field, value in data.items():
            if value is not None:
                setattr(obj, field, value)
        self.db.commit()
        self.db.refresh(obj)
        return obj

    def delete(self, obj: Receipt):
        self.db.delete(obj)
        self.db.commit()


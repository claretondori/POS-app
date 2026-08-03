from sqlalchemy import Column, Integer, Numeric, ForeignKey
from sqlalchemy.orm import relationship, Session

from app.models.sale_item import SaleItem


class SaleItemRepository:
    def __init__(self, db: Session):
        self.db = db

    def get(self, sale_item_id: int):
        return self.db.query(SaleItem).filter(SaleItem.sale_item_id == sale_item_id).first()

    def get_by_sale(self, sale_id: int):
        return self.db.query(SaleItem).filter(SaleItem.sale_id == sale_id).all()

    def get_all(self, skip: int = 0, limit: int = 100):
        return self.db.query(SaleItem).offset(skip).limit(limit).all()

    def create(self, data: dict):
        obj = SaleItem(**data)
        self.db.add(obj)
        self.db.commit()
        self.db.refresh(obj)
        return obj

    def delete(self, obj: SaleItem):
        self.db.delete(obj)
        self.db.commit()


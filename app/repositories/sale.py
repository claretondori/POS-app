import enum

from sqlalchemy.orm import relationship, Session

from app.models.sale import Sale

class SaleStatus(str, enum.Enum):
    completed = "completed"
    voided = "voided"
    refunded = "refunded"




class SaleRepository:
    def __init__(self, db: Session):
        self.db = db

    def get(self, sale_id: int):
        return self.db.query(Sale).filter(Sale.sale_id == sale_id).first()

    def get_all(self, skip: int = 0, limit: int = 100):
        return self.db.query(Sale).offset(skip).limit(limit).all()

    def create(self, data: dict):
        obj = Sale(**data)
        self.db.add(obj)
        self.db.commit()
        self.db.refresh(obj)
        return obj

    def update(self, obj: Sale, data: dict):
        for field, value in data.items():
            if value is not None:
                setattr(obj, field, value)
        self.db.commit()
        self.db.refresh(obj)
        return obj

    def delete(self, obj: Sale):
        self.db.delete(obj)
        self.db.commit()


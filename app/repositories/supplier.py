from sqlalchemy.orm import relationship, Session



from app.models.supplier import Supplier


class SupplierRepository:
    def __init__(self, db: Session):
        self.db = db

    def get(self, supplier_id: int):
        return self.db.query(Supplier).filter(Supplier.supplier_id == supplier_id).first()

    def get_all(self, skip: int = 0, limit: int = 100):
        return self.db.query(Supplier).offset(skip).limit(limit).all()

    def create(self, data: dict):
        obj = Supplier(**data)
        self.db.add(obj)
        self.db.commit()
        self.db.refresh(obj)
        return obj

    def update(self, obj: Supplier, data: dict):
        for field, value in data.items():
            if value is not None:
                setattr(obj, field, value)
        self.db.commit()
        self.db.refresh(obj)
        return obj

    def delete(self, obj: Supplier):
        self.db.delete(obj)
        self.db.commit()


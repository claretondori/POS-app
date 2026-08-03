from sqlalchemy.orm import relationship, Session
from app.models.product import Product



class ProductRepository:
    def __init__(self, db: Session):
        self.db = db

    def get(self, product_id: int):
        return self.db.query(Product).filter(Product.product_id == product_id).first()

    def get_by_sku(self, sku: str):
        return self.db.query(Product).filter(Product.sku == sku).first()

    def get_all(self, skip: int = 0, limit: int = 100):
        return self.db.query(Product).offset(skip).limit(limit).all()

    def get_low_stock(self):
        return (
            self.db.query(Product)
            .filter(Product.reorder_level.isnot(None))
            .filter(Product.quantity_in_stock <= Product.reorder_level)
            .all()
        )

    def create(self, data: dict):
        obj = Product(**data)
        self.db.add(obj)
        self.db.commit()
        self.db.refresh(obj)
        return obj

    def update(self, obj: Product, data: dict):
        for field, value in data.items():
            if value is not None:
                setattr(obj, field, value)
        self.db.commit()
        self.db.refresh(obj)
        return obj

    def delete(self, obj: Product):
        self.db.delete(obj)
        self.db.commit()


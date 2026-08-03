from sqlalchemy.orm import relationship, Session
from app.models.customer import Customer



class CustomerRepository:
    def __init__(self, db: Session):
        self.db = db

    def get(self, customer_id: int):
        return self.db.query(Customer).filter(Customer.customer_id == customer_id).first()

    def get_all(self, skip: int = 0, limit: int = 100):
        return self.db.query(Customer).offset(skip).limit(limit).all()

    def create(self, data: dict):
        obj = Customer(**data)
        self.db.add(obj)
        self.db.commit()
        self.db.refresh(obj)
        return obj

    def update(self, obj: Customer, data: dict):
        for field, value in data.items():
            if value is not None:
                setattr(obj, field, value)
        self.db.commit()
        self.db.refresh(obj)
        return obj

    def delete(self, obj: Customer):
        self.db.delete(obj)
        self.db.commit()


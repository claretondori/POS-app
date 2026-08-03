from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.repositories.customer import CustomerRepository
from app.schemas import customer as schemas


class CustomerService:
    def __init__(self, db: Session):
        self.repo = CustomerRepository(db)

    def list(self, skip: int = 0, limit: int = 100):
        return self.repo.get_all(skip, limit)

    def get(self, customer_id: int):
        obj = self.repo.get(customer_id)
        if not obj:
            raise HTTPException(status.HTTP_404_NOT_FOUND, "Customer not found")
        return obj

    def create(self, data: schemas.CustomerCreate):
        return self.repo.create(data.model_dump())

    def update(self, customer_id: int, data: schemas.CustomerUpdate):
        obj = self.get(customer_id)
        return self.repo.update(obj, data.model_dump(exclude_unset=True))

    def delete(self, customer_id: int):
        obj = self.get(customer_id)
        self.repo.delete(obj)


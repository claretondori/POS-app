from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.repositories.sale_item import SaleItemRepository
from app.repositories.sale import SaleRepository
from app.repositories.product import ProductRepository
from app.schemas import sale_item as schemas


class SaleItemService:
    def __init__(self, db: Session):
        self.db = db
        self.repo = SaleItemRepository(db)
        self.sale_repo = SaleRepository(db)
        self.product_repo = ProductRepository(db)

    def list(self, skip: int = 0, limit: int = 100):
        return self.repo.get_all(skip, limit)

    def list_for_sale(self, sale_id: int):
        return self.repo.get_by_sale(sale_id)

    def get(self, sale_item_id: int):
        obj = self.repo.get(sale_item_id)
        if not obj:
            raise HTTPException(status.HTTP_404_NOT_FOUND, "Sale item not found")
        return obj

    def create(self, data: schemas.SaleItemCreate):
        sale = self.sale_repo.get(data.sale_id)
        if not sale:
            raise HTTPException(status.HTTP_400_BAD_REQUEST, "Sale does not exist")
        product = self.product_repo.get(data.product_id)
        if not product:
            raise HTTPException(status.HTTP_400_BAD_REQUEST, "Product does not exist")
        if product.quantity_in_stock < data.quantity:
            raise HTTPException(
                status.HTTP_400_BAD_REQUEST,
                f"Insufficient stock for '{product.name}' (have {product.quantity_in_stock}, need {data.quantity})",
            )

        subtotal = product.unit_price * data.quantity
        item = self.repo.create({
            "sale_id": data.sale_id,
            "product_id": data.product_id,
            "quantity": data.quantity,
            "unit_price": product.unit_price,
            "subtotal": subtotal,
        })

        product.quantity_in_stock -= data.quantity
        sale.total_amount = (sale.total_amount or 0) + subtotal
        self.db.commit()
        self.db.refresh(item)
        return item

    def update(self, sale_item_id: int, data: schemas.SaleItemUpdate):
        item = self.get(sale_item_id)
        if data.quantity is None or data.quantity == item.quantity:
            return item

        sale = self.sale_repo.get(item.sale_id)
        product = self.product_repo.get(item.product_id)

        delta = data.quantity - item.quantity  # positive = need MORE stock
        if delta > 0 and product.quantity_in_stock < delta:
            raise HTTPException(status.HTTP_400_BAD_REQUEST, f"Insufficient stock for '{product.name}'")

        product.quantity_in_stock -= delta
        new_subtotal = product.unit_price * data.quantity
        sale.total_amount = sale.total_amount - item.subtotal + new_subtotal

        item.quantity = data.quantity
        item.unit_price = product.unit_price
        item.subtotal = new_subtotal

        self.db.commit()
        self.db.refresh(item)
        return item

    def delete(self, sale_item_id: int):
        item = self.get(sale_item_id)
        sale = self.sale_repo.get(item.sale_id)
        product = self.product_repo.get(item.product_id)
        if product:
            product.quantity_in_stock += item.quantity
        if sale:
            sale.total_amount -= item.subtotal
        self.repo.delete(item)


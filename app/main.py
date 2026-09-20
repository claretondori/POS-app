from fastapi import FastAPI


from app.routers import category, customer, payment, products, receipt, sale, sale_item, supplier, user
from app.database import Base, engine

Base.metadata.create_all(bind=engine)

app = FastAPI(title="POS API", version="1.0.0")

app.include_router(category.router)
app.include_router(supplier.router)
app.include_router(products.router)
app.include_router(user.router)
app.include_router(customer.router)
app.include_router(sale.router)
app.include_router(sale_item.router)
app.include_router(payment.router)
app.include_router(receipt.router)


@app.get("/")
def root():
    return {"message": "Welcome to Clare's Point of Sale System API"}


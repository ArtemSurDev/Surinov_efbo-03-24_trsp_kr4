from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from .database import get_db, engine, Base
from .models import Product

Base.metadata.create_all(bind=engine)

app = FastAPI()

@app.get("/products")
def get_products(db: Session = Depends(get_db)):
    products = db.query(Product).all()
    return products

@app.post("/products")
def create_product(title: str, price: int, count: int, description: str, db: Session = Depends(get_db)):
    product = Product(title=title, price=price, count=count, description=description)
    db.add(product)
    db.commit()
    db.refresh(product)
    return product

@app.on_event("startup")
def startup():
    db = next(get_db())
    products = db.query(Product).count()
    if products == 0:
        product1 = Product(title="Product 1", price=100, count=10, description="First product")
        product2 = Product(title="Product 2", price=200, count=5, description="Second product")
        db.add(product1)
        db.add(product2)
        db.commit()
    db.close()

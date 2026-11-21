from fastapi import FastAPI, Depends, HTTPException
import models
from database import engine, SessionLocal
from sqlalchemy.orm import Session
from pydantic import BaseModel
from datetime import datetime
from typing import Annotated

app = FastAPI()
models.Base.metadata.create_all(bind= engine)


class Product(BaseModel):
    produvt_id : int
    product_name : str 
    product_description : str
    product_price : float

class User(BaseModel):
    username : str
    name: str 
    email: str
    is_admin: bool
    phone_number : int

class Category(BaseModel):
    category_id :int
    category_description: str

class Order(BaseModel):
    order_id: int
    order_name: str
    order_date: datetime
    order_desciption: str


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependancy = Annotated[dict, Depends(get_db())]

#the home page
@app.get("/home")
async def home_page(message : str):
    return {message : "Welcome to the mini store"}

#viewing the product 
@app.get("/peoducts")
async def view_products(db : Session = Depends(get_db)):
    products = db.query(models.Product).all()
    return products

#adding products
@app.post("/add_products")
async def add_products(product: Product, db : Session = Depends(get_db)):
    new_product = models.Product(
        product_name = product.product_name,
        product_description = product.product_description,
        product_price = product.product_price
    )
    db.add(new_product)
    db.commit()
    db.refresh(new_product)
    return {"message":"Product added successfully","product":new_product}

#update product
@app.put("/update_product/{product_id}")
async def update_product(product_id : int , updated_product: Product, db : Session = Depends(get_db)):
    product = db.query(models.Product).filter(models.Product.product_id == product_id).first()
    if not product:
        return {"error": "Product not found"}
    product.product_name = updated_product.product_name
    product.product_description = updated_product.product_description
    product.product_price = updated_product.product_price
    db.commit()
    db.refresh(product)
    return {"message":"Product updated successfully", "product": product}

# delete product 
@app.delete("/delete_product/{product_id}")
async def delete_product(product_id: int, db : Session = Depends(get_db)):
    product = db.query(models.Product).filter(models.Product.product_id == product_id).first()
    if not product:
        raise HTTPException(status_code = 404, detail = "Product not found")
    db.delete(product)
    db.refresh(product)
    db.commit()
    return {"message": "Product deleted successfully"}

#view users
@app.get("/users")
async def view_users(db: Session = Depends(get_db)):
    users = db.query(models.User).all()
    return users


#create user 
@app.post("/create_user")
async def create_user(user: User, db : Session = Depends(get_db)):
    if db.query(models.User).filter(models.User.username == user.username).first():
        raise HTTPException(status_code=400, detail = "Username already exists")
    else:
        if db.query(models.User).filter(models.User.email == user.email).first():
            raise HTTPException(status_code=400, detail = "Email already exists")
    new_user = models.User(
        username = user.username,
        name = user.name,
        email = user.email,
        is_admin = user.is_admin,
        phone_number = user.phone_number
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {"message":"User created successfully","user": new_user}

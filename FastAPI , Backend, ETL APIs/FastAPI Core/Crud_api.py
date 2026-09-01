import os
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from sqlalchemy import create_engine, Column, Integer, String, Float
from sqlalchemy.orm import declarative_base, sessionmaker
from pydantic import BaseModel
from typing import Optional

load_dotenv()

user = os.getenv("user")
password = os.getenv("password")
host = os.getenv("host")
port = os.getenv("port")
db_name = os.getenv("db_name")

app = FastAPI()

DATABASE_URL = f"mysql+pymysql://{user}:{password}@{host}:{port}/{db_name}"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    email = Column(String(100), nullable=False)
    age = Column(Integer, nullable=False)


class Product(Base):

    __tablename__ = "products"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    description = Column(String(200), nullable=False)
    price = Column(Float, nullable=False)
    quantity = Column(Integer, nullable=False)

Base.metadata.create_all(bind=engine)

class UserCreate(BaseModel):

    name: str
    email: str
    age: int


class UserUpdate(BaseModel):

    name: Optional[str] = None
    email: Optional[str] = None
    age: Optional[int] = None


class UserResponse(BaseModel):

    id: int
    name: str
    email: str
    age: int

    class Config:
        orm_mode = True

class ProductCreate(BaseModel):

    name: str
    description: str
    price: float
    quantity: int


class ProductUpdate(BaseModel):

    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None
    quantity: Optional[int] = None


class ProductResponse(BaseModel):

    id: int
    name: str
    description: str
    price: float
    quantity: int

    class Config:
        orm_mode = True

@app.get("/users", response_model=list[UserResponse])

def get_users():

    db = SessionLocal()
    users = db.query(User).all()
    db.close()
    return users

@app.get("/users/get-id/{name}")
def get_user_id(name: str):

    db = SessionLocal()

    user = db.query(User).filter(User.name == name).first()

    if not user:
        db.close()
        raise HTTPException(status_code=404, detail="User not found")

    db.close()

    return {
        "id": user.id,
        "name": user.name
    }

@app.post("/users")

def add_user(user: UserCreate):

    db = SessionLocal()
    new_user = User(**user.dict())
    db.add(new_user)
    db.commit()
    db.close()

    return {"message": "User added successfully"}

@app.put("/users/{id}")

def update_user(id: int, user: UserCreate):

    db = SessionLocal()
    old_user = db.query(User).filter(User.id == id).first()

    if not old_user:

        db.close()
        raise HTTPException(status_code=404, detail="User not found")

    old_user.name = user.name
    old_user.email = user.email
    old_user.age = user.age

    db.commit()
    db.close()
    return {"message": "User updated successfully"}

@app.patch("/users/{id}", response_model=UserResponse)

def patch_user(id: int, user: UserUpdate):
    db = SessionLocal()
    old_user = db.query(User).filter(User.id == id).first()

    if not old_user:
        db.close()
        raise HTTPException(status_code=404, detail="User not found")

    update_data = user.dict(exclude_unset=True)

    for key, value in update_data.items():

        setattr(old_user, key, value)

    db.commit()
    db.refresh(old_user)
    db.close()

    return old_user

@app.delete("/users/{id}")

def delete_user(id: int):
    db = SessionLocal()
    user = db.query(User).filter(User.id == id).first()
    if not user:
        db.close()
        raise HTTPException(status_code=404, detail="User not found")

    db.delete(user)
    db.commit()
    db.close()

    return {"message": "User deleted successfully"}

@app.get("/products", response_model=list[ProductResponse])

def get_products():
    db = SessionLocal()
    products = db.query(Product).all()
    db.close()
    return products

@app.get("/products/get-id/{name}")
def get_product_id(name: str):

    db = SessionLocal()

    product = db.query(Product).filter(Product.name == name).first()

    if not product:
        db.close()
        raise HTTPException(status_code=404, detail="Product not found")

    db.close()

    return {
        "id": product.id,
        "name": product.name
    }

@app.post("/products")

def add_product(product: ProductCreate):

    db = SessionLocal()
    new_product = Product(**product.dict())
    db.add(new_product)
    db.commit()
    db.close()

    return {"message": "Product added successfully"}

@app.put("/products/{id}")

def update_product(id: int, product: ProductCreate):
    db = SessionLocal()
    old_product = db.query(Product).filter(Product.id == id).first()
    if not old_product:

        db.close()
        raise HTTPException(status_code=404, detail="Product not found")

    old_product.name = product.name
    old_product.description = product.description
    old_product.price = product.price
    old_product.quantity = product.quantity

    db.commit()
    db.close()

    return {"message": "Product updated successfully"}

@app.patch("/products/{id}", response_model=ProductResponse)

def patch_product(id: int, product: ProductUpdate):

    db = SessionLocal()

    old_product = db.query(Product).filter(Product.id == id).first()
    if not old_product:

        db.close()
        raise HTTPException(status_code=404, detail="Product not found")

    update_data = product.dict(exclude_unset=True)

    for key, value in update_data.items():
        setattr(old_product, key, value)

    db.commit()
    db.refresh(old_product)
    db.close()
    return old_product

@app.delete("/products/{id}")

def delete_product(id: int):
    db = SessionLocal()
    product = db.query(Product).filter(Product.id == id).first()

    if not product:
        db.close()

        raise HTTPException(status_code=404, detail="Product not found")

    db.delete(product)
    db.commit()
    db.close()
    return {"message": "Product deleted successfully"}
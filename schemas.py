from pydantic import BaseModel
from typing import Optional

class Base(BaseModel):
    name: str
    description: str
    class Config:
        from_attributes = True

    
class Product(Base):
    id:int
    vendor_code: str
    price: float
    category_id: int

class CreateProduct(Base):
    vendor_code: str
    price: float
    category_id: int

class CreateProduct(Base):
    id: int

class Category(Base):
    id:int
    type_id: int

class Type(Base):
    id: int
    pass

class ProductImage(BaseModel):
    name: str
    product_id: int
    vendor_code:str
    
    class Config:
        from_attributes = True



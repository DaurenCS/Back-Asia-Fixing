from pydantic import BaseModel
from typing import Optional, List

class Base(BaseModel):
    name: str
    description: str
    local : str
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

class Type(Base):
    id:int

class Category(Base):
    type_id: int
    image: str



class ProductImage(BaseModel):
    name: str
    product_id: int
    vendor_code:str
    
    class Config:
        from_attributes = True


class ProductDetails(Base):
    id: int
    vendor_code: str   
    price: float
    category: Category
    images: ProductImage

class Technology(Base):
    name:str
    description:str
    image:str
    text:str
    local:str
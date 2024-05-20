from pydantic import BaseModel
from typing import Optional, List

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

class Type(Base):
    id: int
    pass

class Category(Base):
    id:int
    type: Type



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
    images: List[ProductImage]
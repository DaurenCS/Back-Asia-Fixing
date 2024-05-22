from typing import Annotated

import sqlalchemy 
from sqlalchemy.orm import mapped_column, Mapped, relationship
from sqlalchemy.ext.associationproxy import association_proxy

from database import Base

_id = Annotated[int, mapped_column(sqlalchemy.Integer, primary_key=True)]


class Product(Base):
    __tablename__ = "products"

    id : Mapped[_id]
    vendor_code: Mapped[str]
    name: Mapped[str]
    description: Mapped[str]
    price: Mapped[float]
    
    category_id: Mapped[int] = mapped_column(sqlalchemy.ForeignKey('categories.id'))
    category: Mapped['Category'] =  relationship(back_populates='product')

    images: Mapped['ProductImage'] = relationship(back_populates='product',uselist=True)

class ProductImage(Base):
    __tablename__ = "images"
    id : Mapped[_id]
    name: Mapped[str]
    product_id: Mapped[int] = mapped_column(sqlalchemy.ForeignKey('products.id'))
    

    product: Mapped['Product'] =  relationship(back_populates='images')
    vendor_code = association_proxy("product", "vendor_code")

    


class Category(Base):
    __tablename__ = "categories"
    id : Mapped[_id]
    name: Mapped[str]
    description: Mapped[str]
    
    type_id: Mapped[int] = mapped_column(sqlalchemy.ForeignKey('types.id'))
    type: Mapped['Type'] =  relationship(back_populates='category')

    product: Mapped[Product] =  relationship(back_populates='category')




    

class Type(Base):
    __tablename__ = "types"
    id : Mapped[_id]
    name: Mapped[str]
    description: Mapped[str]

    category: Mapped['Category'] =  relationship(back_populates='type', uselist=True)


class Technology(Base):
    __tablename__ = "technologies"
    id: Mapped[_id]
    name: Mapped[str]
    description: Mapped[str]
    image: Mapped[str]
    text: Mapped[str]
    local: Mapped[str] 








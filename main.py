from fastapi import FastAPI, Depends
from sqlalchemy import select, insert
import schemas as sch
import database as db
import models as mdl
from fastapi import HTTPException
from sqlalchemy.future import select
from sqlalchemy.orm import Session, selectinload
from database import session
from typing import List
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)

def get_db():
    try:
        yield session
        session.commit()
    except:
        raise
    finally:
        session.close()

def url_creater(product: sch.Product):
    replaced_string = product.name.replace(".", "_").replace(" ", "-")
    result = f"https://inkafixing.com/Uploads/images/Products/{product.vendor_code}/{replaced_string}.jpg"
    urls = []
    urls.append(result)
    list = [1,2,3]
    for i in list:
        result = f"https://inkafixing.com/Uploads/images/Products/{product.vendor_code}/{replaced_string}-{i}.jpg"
        urls.append(result)
    return urls


@app.post("/products/add")
def add_product(product: sch.Product, session: Session = Depends(get_db)) -> str:
    db_product  = mdl.Product(**product.model_dump())
    session.add(db_product)
    for url in url_creater(product):
        images = mdl.ProductImage(product_id = product.id, name = url)
        session.add(images)
    return f"Products was added;"

@app.get("/products", response_model=List[sch.ProductDetails])
def get_products(session: Session = Depends(get_db)):
    # Query to get list of products with details including category name, type name, and product images
    products = (
        session.query(mdl.Product)
        .options(
            selectinload(mdl.Product.category).selectinload(mdl.Category.type),
            selectinload(mdl.Product.images)
        )
        .all()
    )
    
    return products


@app.post("/categories/add")
def add_category(category: sch.Category, session: Session = Depends(get_db)) -> str:
    session.add(mdl.Category(**category.model_dump()))
    return "Category was added"

@app.get("/categories")
def get_categories( session: Session = Depends(get_db)):
    db_products = session.query(mdl.Category).all()
    return [sch.Category.model_validate(product) for product in db_products]


@app.post("/types/add")
def add_type(type: sch.Type, session: Session = Depends(get_db)) -> str:
    session.add(mdl.Type(**type.model_dump()))
    return "Type was added"

@app.get("/types")
def get_type( session: Session = Depends(get_db)):
    db_products = session.query(mdl.Type).all()
    return [sch.Type.model_validate(product) for product in db_products]

@app.get("/product/{product_id}/images")
def get_images(product_id: int, session: Session = Depends(get_db)):
    product_images = session.query(mdl.ProductImage).filter(mdl.ProductImage.product_id == product_id).all()
    return [sch.ProductImage.model_validate(items) for items in product_images]


    
@app.get("/products/isolation/categories")
def get_hidro_isolation(session: Session = Depends(get_db)):
    types = session.query(mdl.Type).filter(mdl.Type.name == "HidroIsolation").first()
    categories = session.query(mdl.Category).filter(mdl.Category.type_id == types.id).all()
    return [sch.Category.model_validate(items) for items in categories]


@app.get("/products/{category_id}")
def get_products_by_category(category_id: int, session: Session = Depends(get_db)):
    products = session.query(mdl.Product).filter(mdl.Product.category_id == category_id).all()
    return [sch.Product.model_validate(items) for items in products]

@app.get("/categories/{type_id}")
def get_categories_by_type_id(type_id: int, session: Session = Depends(get_db)):
    categories = session.query(mdl.Category).filter(mdl.Category.type_id == type_id).all()
    return [sch.Category.model_validate(items) for items in categories]
    


@app.get("/products/type/{type_id}")
def get_products_by_type_id(type_id: int, session: Session = Depends(get_db)):
    db_query = (
        select(mdl.Product)
        .join(mdl.Category)
        .join(mdl.Type)
        .where(mdl.Type.id == type_id)
    )
    products = session.execute(db_query).scalars().all()
    if not products:
        raise HTTPException(status_code=404, detail="No products found for the given type ID")
    
    return products


@app.get("/products/{product_id}", response_model=sch.ProductDetails)
def get_product_details(product_id: int, session: Session = Depends(get_db)):
    # Query to get product details with category name, type name, and product images
    product = (
        session.query(mdl.Product)
        .options(
            selectinload(mdl.Product.category).selectinload(mdl.Category.type),
            selectinload(mdl.Product.images)
        )
        .filter(mdl.Product.id == product_id)
        .first()
    )
    
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    
    return product
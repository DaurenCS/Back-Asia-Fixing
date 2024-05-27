from fastapi import FastAPI, Depends, status
from sqlalchemy import select, insert
import schemas as sch
import database as db
import models as mdl
from fastapi import HTTPException, UploadFile, File
from sqlalchemy.future import select
from sqlalchemy.orm import Session, selectinload, joinedload
from database import sessionLocal
from typing import List
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.exc import SQLAlchemyError, NoResultFound
from fastapi.responses import FileResponse
import shutil
import os

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)

async def get_db():
    session = sessionLocal()
    try:
        yield session
        session.commit()
    except Exception as e:
        session.rollback()
        raise
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

@app.post("/technologies/add")
def add_technologies(product: sch.Technology, session: Session = Depends(get_db)) -> str:
    db_product  = mdl.Technology(**product.model_dump())
    session.add(db_product) 
    return f"Technology was added;"

@app.get("/technologies")
def get_technologies(local: str, session: Session = Depends(get_db)):
    db_tech = session.query(mdl.Technology).filter(mdl.Technology.local == local).all() 
    return [sch.Technology.model_validate(tech) for tech in db_tech]


@app.get("/products")
def get_product( local: str, session: Session = Depends(get_db)):
    db_products = session.query(mdl.Product).filter(mdl.Product.local == local).all()
    return [sch.ProductDetails.model_validate(product) for product in db_products]


@app.post("/categories/add")
def add_category(category: sch.Category, session: Session = Depends(get_db)) -> str:
    session.add(mdl.Category(**category.model_dump()))
    return "Category was added"

@app.get("/categories")
def get_categories(local: str, session: Session = Depends(get_db)):
    db_products = session.query(mdl.Category).filter(mdl.Category.local == local).all()
    return [sch.Category.model_validate(product) for product in db_products]


@app.post("/types/add")
def add_type(type: sch.Type, session: Session = Depends(get_db)) -> str:
    session.add(mdl.Type(**type.model_dump()))
    return "Type was added"

@app.get("/types")
def get_type(local: str, session: Session = Depends(get_db)):
    db_products = session.query(mdl.Type).filter(mdl.Type.local == local).filter(mdl.Type.name != "Hidroisolation").all()
    return [sch.Type.model_validate(product) for product in db_products]

@app.get("/product/{product_id}/images")
def get_images(product_id: int, session: Session = Depends(get_db)):
    product_images = session.query(mdl.ProductImage).filter(mdl.ProductImage.product_id == product_id).all()
    return [sch.ProductImage.model_validate(items) for items in product_images]


    
@app.get("/products/isolation/categories")
def get_hidro_isolation(local: str, session: Session = Depends(get_db)):
    try:
        types = session.query(mdl.Type).filter(mdl.Type.local == local).filter(mdl.Type.name == "Hidroisolation").first()
        
        if not types:
            raise HTTPException(status_code=404, detail="Type 'HidroIsolation' not found")

        categories = session.query(mdl.Category).filter(mdl.Category.type_id == types.id).all()

        if not categories:
            raise HTTPException(status_code=404, detail="No categories found for type 'HidroIsolation'")

        return [sch.Category.model_validate(items) for items in categories]
    
    except HTTPException as http_exc:
        raise http_exc

    except Exception as e:
        print(f"Unexpected error: {e}")
        raise HTTPException(
            status_code=500,
            detail="Internal server error"
        )


@app.get("/products/category/{category_id}")
def get_products_by_category(category_id: int, session: Session = Depends(get_db)):
    products = session.query(mdl.Product).filter(mdl.Product.category_id == category_id).all()
    return [sch.ProductDetails.model_validate(items) for items in products]

@app.get("/categories/{type_id}")
def get_categories_by_type_id(type_id: int, session: Session = Depends(get_db)):
    try:
        categories = session.query(mdl.Category).filter(mdl.Category.type_id == type_id).all()
        if not categories:
            return {"not found"}
        return [sch.Category.model_validate(items) for items in categories]
    except SQLAlchemyError as e:
        print(f"Database error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )
    except Exception as e:
        print(f"Unexpected error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )


@app.get("/types-with-categories")
def get_types_with_categories(local: str, session: Session = Depends(get_db)):
    try:
        types = session.query(mdl.Type).filter(mdl.Type.local == local).filter(mdl.Type.name != "Hidroisolation").all()
        
        if not types:
            raise HTTPException(status_code=404, detail="No types found")

        return [
            {
                "id": type.id,
                "name": type.name,
                "description": type.description,
                "categories": get_categories_by_type_id(type.id, session)
            } for type in types
        ]
    except Exception as e:
        print(f"Unexpected error: {e}")
        raise HTTPException(
            status_code=500,
            detail="Internal server error"
        )

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
    
    return [sch.ProductDetails.model_validate(items) for items in products]


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


@app.post("/upload")
async def upload_files(file: UploadFile = File(...)):
    file_path = f"images/{file.filename}"
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    return {"file" : file_path}

@app.get("/upload/{file_name}")
async def get_files_by_name(file_name:str):
    path = os.path.join("images/", file_name)
    if not os.path.isfile(path):
        raise HTTPException(status_code=404, detail="File not found")
    
    return FileResponse(path)
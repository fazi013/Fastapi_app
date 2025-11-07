from fastapi import FastAPI,Depends,HTTPException
from model import Products,ProductCreate,ProductOut,ProductUpdate
from sqlalchemy.orm import Session
from database import SessionLocal,engine
from databasemodel import Product
import databasemodel


app = FastAPI()

databasemodel.Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
def read_root(db:Session= Depends(get_db),response_model=ProductOut):
    db_products= db.query(databasemodel.Product).all()
    return db_products




@app.post("/Add_products",response_model=ProductOut)
def add_product(Pro:ProductCreate,db:set=Depends(get_db)):
    new_pro= Product(**Pro.dict())
    db.add(new_pro)
    db.commit()
    db.refresh(new_pro)
    return new_pro



@app.get("/products/{product_id}",response_model=ProductOut)
def get_products(product_id:int,db:Session=Depends(get_db)):
    item= db.query(Product).filter(Product.id==product_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Product not found")
   
    return item



@app.put("/update")
def get_products(product_id:int,update:ProductUpdate,db:Session=Depends(get_db)):
    item= db.query(Product).filter(Product.id==product_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Product not found")
    item.name=update.name
    item.description=update.description
    item.price = update.price
    item.quantity=update.quantity
    db.commit()
    return{"message:updated succesfuly"}
    






@app.delete("/delete/{product_id}")
def delete(product_id:int,db:Session=Depends(get_db)):
     item= db.query(Product).filter(Product.id==product_id).first()
     if not item:
        raise HTTPException(status_code=404, detail="Product not found")
     db.delete(item)
     db.commit()
     return {"message": "Product deleted successfully"}






from fastapi import FastAPI, Request, Form
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from bson import ObjectId
from database import task_collection
from model import Task

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

@app.get("/")
async def task_list(request: Request):
    tasks = await task_collection.find().to_list(100)
    for task in tasks:
        task["_id"] = str(task["_id"])
    return templates.TemplateResponse("task_list.html", {"request": request, "tasks": tasks})

@app.get("/task/add")
def task_add_form(request: Request):
    return templates.TemplateResponse("task_form.html", {"request": request, "task": None})

@app.post("/task/add")
async def task_add(title: str = Form(...), description: str = Form("")):
    task = Task(title=title, description=description)
    await task_collection.insert_one(task.dict())
    return RedirectResponse("/", status_code=303)

@app.get("/task/edit/{task_id}")
async def task_edit_form(request: Request, task_id: str):
    task = await task_collection.find_one({"_id": ObjectId(task_id)})
    task["_id"] = str(task["_id"])
    return templates.TemplateResponse("task_form.html", {"request": request, "task": task})

@app.post("/task/edit/{task_id}")
async def task_edit(task_id: str, title: str = Form(...), description: str = Form("")):
    await task_collection.update_one({"_id": ObjectId(task_id)}, {"$set": {"title": title, "description": description}})
    return RedirectResponse("/", status_code=303)

@app.post("/task/delete/{task_id}")
async def task_delete(task_id: str):
    await task_collection.delete_one({"_id": ObjectId(task_id)})
    return RedirectResponse("/", status_code=303)

@app.post("/task/toggle/{task_id}")
async def task_toggle(task_id: str):
    task = await task_collection.find_one({"_id": ObjectId(task_id)})
    await task_collection.update_one({"_id": ObjectId(task_id)}, {"$set": {"completed": not task["completed"]}})
    return RedirectResponse("/", status_code=303)


























'''from fastapi import FastAPI,Depends,HTTPException
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



'''


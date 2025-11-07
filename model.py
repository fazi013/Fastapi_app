from pydantic import BaseModel

class Products (BaseModel):
     #id: int
     name: str
     description: str
     price: float
     quantity: int

class ProductCreate(Products):
    pass

class ProductUpdate(Products):
    pass

class ProductOut(Products):
    id: int

    class Config:
        orm_mode = True

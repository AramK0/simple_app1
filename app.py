from fastapi import FastAPI
from pydantic import BaseModel
from databases import Database
from sqlalchemy import create_engine, MetaData, Table, Column, String
from dotenv import load_dotenv
import os

DATABASE_URL = os.getenv("DATABASE_URL")
print(os.getenv("DATABASE_URL"))
load_dotenv()

database = Database(DATABASE_URL)
metadata = MetaData()

products = Table("products", metadata, Column("item", String, primary_key=True),)
engine = create_engine(DATABASE_URL)
metadata.create_all(engine)


app = FastAPI()

class product(BaseModel):
    item: str

@app.on_event("startup")
async def startup():
    await database.connect()

@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()


@app.get("/")
async def home():
    return {"status": "hello"}

@app.post('/items/')
async def create_items(product: product):
    query = products.insert().values(item=product.item)
    await database.execute(query)
    return {"Your item is": product.item}

@app.get("/items/")
async def read_items():
    query = products.select()
    rows = await database.fetch_all(query)
    return rows



from pydantic import BaseModel
from fastapi import FastAPI


class Item(BaseModel):
    name: str
    description: str = None
    price: float
    tax: float = None


app = FastAPI()


# body Parameter
@app.post("/items")
async def create_item(item: Item):
    return item


# combining query, path and body parameters
@app.put("/items/{item_id}")
async def put_item(item_id: int, item: Item, importance: int = 1):
    return {"item_id": item_id, "item": item, "importance": importance}

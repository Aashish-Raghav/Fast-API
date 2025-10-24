from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, Field
from typing import Optional

# Database ( in - memory for this example)
item_db = {}
next_id = 1


# Models
class ItemCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    description: Optional[str] = None
    price: float = Field(..., gt=0)


class ItemResponse(BaseModel):
    id: int
    name: str
    description: Optional[str] = None
    price: float


app = FastAPI()


# CREATE
@app.post("/items", response_model=ItemResponse, status_code=status.HTTP_201_CREATED)
async def create_item(item: ItemCreate):
    global next_id
    item_id = next_id
    next_id += 1
    item_db[item_id] = {"id": item_id, **item.model_dump()}
    return item_db[item_id]


# FETCH
@app.get("/items/{item_id}")
async def fetch_item(item_id: int):
    if item_id not in item_db:
        raise HTTPException(status_code=404, detail="Item not found")
    return item_db[item_id]


# FETCH ALL
@app.get("/items", response_model=list[ItemResponse])
async def fetch_items(skip: int = 0, limit: int = 10):
    return list(item_db.values())[skip : skip + limit]


# UPDATE
@app.put("/items/{item_id}", response_model=ItemResponse)
async def update_item(item_id: int, item: ItemCreate):
    if item_id not in item_db:
        raise HTTPException(status_code=404, detail="Item not Found")

    item_db[item_id].update(item.model_dump(exclude_unset=True))
    return item_db[item_id]


# DELETE
@app.delete("/items/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_item(item_id: int):
    if item_id not in item_db:
        raise HTTPException(status_code=404, detail="Item not Found")

    del item_db[item_id]
    return None

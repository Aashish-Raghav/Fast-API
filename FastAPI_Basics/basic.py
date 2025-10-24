from fastapi import FastAPI

app = FastAPI()


# Basic HTTP methods
@app.get("/")
async def read_root():
    return {"message": "Hello, World!"}


@app.post("/items")
async def post_item():
    return "POST Request"


# Path Parameters with type validation
@app.put("/items/{item_id}")
async def put_item(item_id: int):
    return f"PUT Request {item_id}"


@app.delete("/items/{item_id}")
async def delete_item(item_id: int):
    return f"Delete Request {item_id}"


# Query Parameters
@app.get("/items/")
async def get_item(skip: int = 0, limit: int = 10):
    return {"Request type ": "GET", "skip": skip, "limit": limit}

from pydantic import BaseModel, Field
from typing import Optional
from fastapi import FastAPI, status

app = FastAPI()


# Nested Models
class Address(BaseModel):
    street: str
    city: str
    country: str


class User(BaseModel):
    name: str
    email: str
    address: Address


# Optional Field and Values
class Product(BaseModel):
    name: str  # Required
    description: str = "No description"  # Optional with default
    price: float  # Required
    in_stock: bool = True  # Optional with default
    tags: Optional[list] = None  # Optional, defaults to None


# Field Validation
class Item(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    price: float = Field(..., gt=0, description="Price must be greater than 0")
    quantity: int = Field(default=1, ge=0, description="Quantity must be >= 0")
    description: Optional[str] = None


"""
The Field function provides additional validation constraints:

    gt / ge: Greater than / greater than or equal
    lt / le: Less than / less than or equal
    min_length / max_length: String length constraints
    ... (ellipsis): Marks a field as required
"""


# custom status with Models
@app.post("/items", status_code=status.HTTP_201_CREATED)
async def create_item(item: Item):
    """
    Create an item by ID.

    - **item_id**: The unique identifier of the item
    """
    return item


# Response Model
class ItemResponse(BaseModel):
    id: int
    name: str
    price: float


@app.get("/item/{item_id}", response_model=ItemResponse)
async def get_item(item_id: int):
    # simulate database search

    # return {"id" : item_id, "name" : "item", "price" : 10}
    return ItemResponse(id=item_id, name="item1", price=10)

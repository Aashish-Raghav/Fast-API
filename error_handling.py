from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse


# ---- Define common error base ----
class AppError(Exception):
    def __init__(self, message: str, status_code: int = 400):
        self.message = message
        self.status_code = status_code


class ItemNotFoundError(AppError):
    def __init__(self, item_id: int):
        super().__init__(f"Item with id {item_id} not found", status_code=404)


# ---- Exception handler ----
app = FastAPI()


@app.exception_handler(AppError)
async def app_error_handler(request: Request, exc: AppError):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": exc.__class__.__name__,
            "message": exc.message,
            "path": str(request.url),
        },
    )


@app.get("/item/{item_id}")
async def get_item(item_id: int):
    if item_id not in [1, 2, 3]:
        raise ItemNotFoundError(item_id)
    return {"item_id": item_id}


"""
✅ Advantages:
    Centralized error response format
    Customizable exception hierarchy
    Standardized logging/monitoring possible
    Extensible (e.g., plug in Sentry, Prometheus, etc.)
"""

from fastapi import HTTPException


@app.get("/items_http_exception/{item_id}")
async def get_item(item_id: int):
    if item_id not in [1, 2, 3]:
        raise HTTPException(status_code=404, detail="Item not found")


"""
✅ Pros
    Simpler and built-in — no boilerplate
    Automatically generates proper OpenAPI response
    Great for small-to-medium projects or one-off checks
    Works well when only a few exception types are used

❌ Cons
    Becomes repetitive if the same type of error is raised in multiple places
    You can't easily attach custom context (like path, request info, metadata)
    Harder to standardize error format across APIs (e.g., for a microservice system)
"""

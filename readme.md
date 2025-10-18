# FastAPI Basics: A Complete Guide

## Introduction
FastAPI is a modern, high-performance web framework for building APIs with Python 3.7+.  
It provides automatic interactive API documentation, data validation/serialization, and sensible error handling out of the box.

## Why FastAPI over Flask or Django?
- Flask: lightweight and flexible but requires manual validation, serialization, and docs setup for larger APIs.  
- Django: full-featured for web apps but heavier than necessary for API-only services.  
- FastAPI advantages:
  - Automatic validation via Pydantic
  - First-class use of Python type hints
  - Auto-generated interactive docs (Swagger UI and ReDoc)
  - High performance (async support, comparable to Node/Go)
  - Built-in request/response validation and error handling
  - Less boilerplate → faster developer productivity

## Quick Start — Installation
Run on Windows (PowerShell or CMD):
```bash
pip install fastapi "uvicorn[standard]"
```


## Index

This section lists each example file in this directory. Each entry explains the topic, what is covered, and how to run the example.

1. [Basics](#1-Basics)

---

## 1. Basics

**Purpose:**

- A minimal, focused example to demonstrate FastAPI fundamentals and how function signatures map to HTTP behavior and automatic documentation.

**What we've covered in code:**

- Basic HTTP methods: GET, POST, PUT, DELETE.
- Path parameters with type validation (e.g., integer IDs).
- Query parameters with default values and validation.
- How FastAPI uses Python type hints to parse and validate incoming requests.
- How endpoints appear in the automatically generated API documentation (Swagger UI and ReDoc).

*See: [`basic.py`](basic.py)*


Run on Windows (PowerShell or CMD):
```bash
uvicorn basic:app --reload
```


## Resources
- Official docs: https://fastapi.tiangolo.com  
- Pydantic: https://pydantic-docs.helpmanual.io

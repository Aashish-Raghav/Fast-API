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
2. [Parameters](#2-Parameters)  
3. [Models](#3-Models)
4. [Error Handling](#4-Error-Handling)
5. [Example App](#5-Example-App)
6. [SQLAlchemy](#6-SQLAlchemy-Async-Example)


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

## 2. Parameters

**Purpose:**

- Demonstrates how to define request bodies using Pydantic models and how to combine query, path, and body parameters in endpoint definitions.

**What is covered:**

- Defining Pydantic models for request bodies.
- Body parameter handling and automatic validation.
- Combining path parameters, request body models, and query parameters in one endpoint.
- Default values and optional fields in endpoint signatures.
- How parameter definitions appear in auto-generated docs and are validated at runtime.

*See: [`parameters.py`](parameters.py)*

How to run (Windows PowerShell or CMD):
```bash
uvicorn parameters:app --reload
```

## 3. Models

**Purpose:**

- Shows advanced Pydantic model usage: nested models, optional fields, field validation constraints, default values, and response models coupled with status codes.

**What is covered:**

- Nested models to represent related objects (e.g., Address inside User).
- Optional fields with defaults and how they are documented.
- Field-level validation using Pydantic's Field (constraints like min/max length, greater-than, etc.).
- Using response models to control output shape and validation.
- Setting custom HTTP status codes for endpoints.
- How these model features influence request/response validation and the API docs.

*See: [`models.py`](models.py)*

How to run (Windows PowerShell or CMD):
```bash
uvicorn models:app --reload
```


## 4. Error Handling

**Purpose:**

- Demonstrates patterns for consistent, centralized error handling in FastAPI applications using custom exceptions and exception handlers, and compares that approach with built-in HTTPException usage.

**What is covered:**

- Defining a custom application exception base class and specific exception types.
- Registering exception handlers to return consistent JSON error responses (status code, error type, message, request path).
- Using built-in HTTPException for simpler, inline error responses.
- Trade-offs between centralized custom handlers (standardized format, richer context, easier monitoring/logging) and HTTPException (simplicity, automatic OpenAPI responses).
- Best-practice considerations for production: consistent error schemas, integration with logging/monitoring, and choosing the right approach depending on project complexity.

*See: [`error_handling.py`](error_handling.py)*

How to run (Windows PowerShell or CMD):
```bash
uvicorn error_handling:app --reload
```


## 5. Example App

**Purpose:**

- A compact, practical example demonstrating a small CRUD application built with FastAPI and Pydantic.

**What is covered:**

- Full CRUD endpoints for an Item resource (create, read single, read list, update, delete).
- Request validation using Pydantic models (request and response models).
- Use of HTTP status codes (201 Created, 204 No Content, 404 Not Found).
- In-memory data store pattern for example/testing purposes.
- Pagination-like parameters (skip and limit) for list endpoints.
- Using response_model to shape and validate outgoing responses.

See: [`example.py`](example.py)

How to run (Windows PowerShell or CMD):
```bash
uvicorn example:app --reload
```


## 6. SQLAlchemy Async Example

Purpose:
- Demonstrates integrating FastAPI with asynchronous SQLAlchemy usage and an organized project layout.

What is covered (file roles):
- `SQLalchemy/.env` — Holds DATABASE_URL (example uses sqlite+aiosqlite).  
- `SQLalchemy/app/main.py` — FastAPI app, startup event to create tables, router inclusion.  
- `SQLalchemy/app/database.py` — Async engine setup, async_sessionmaker, declarative Base, get_db dependency, reads .env.  
- `SQLalchemy/app/models.py` — ORM model definitions (SQLAlchemy).  
- `SQLalchemy/app/schemas.py` — Pydantic schemas for request/response with orm_mode.  
- `SQLalchemy/app/crud.py` — Async CRUD helpers using AsyncSession.  
- `SQLalchemy/app/routers/users.py` — APIRouter example showing dependency injection and endpoint signatures.  
- `SQLalchemy/app/version.py` — simple helper printing SQLAlchemy version (diagnostic).  
- `.vscode/launch.json` — example VS Code debug configuration that points to this project and uses the .env file.

Key concepts demonstrated:
- Async SQLAlchemy engine and sessions.
- Dependency injection for DB sessions.
- Separation of models / schemas / crud / routers.
- Creating DB tables at application startup.
- Using environment variables for configuration.

How to run:
- Install required packages
```bash
pip install fastapi uvicorn sqlalchemy sqlalchemy[aysncio] aiosqlite python-dotenv email-validator psycopg2-binary
```
- Start the app
```bash
uvicorn SQLalchemy.app.main:app --reload
```
- Alternatively use the provided VS Code launch configuration to run/debug (ensure python path and virtual env are correct).

Notes:
- The example uses an in-memory / local sqlite URL by default via .env; swap to a production DB for real use.
- database.py prints environment diagnostics to help troubleshoot .env loading.


## Resources
- Official docs: https://fastapi.tiangolo.com  
- Pydantic: https://pydantic-docs.helpmanual.io

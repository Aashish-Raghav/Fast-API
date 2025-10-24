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

*See: [`FastAPI_Basics/basic.py`](FastAPI_Basics/basic.py)*

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

*See: [`FastAPI_Basics/parameters.py`](FastAPI_Basics/parameters.py)*

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

*See: [`FastAPI_Basics/models.py`](FastAPI_Basics/models.py)*

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

*See: [`FastAPI_Basics/error_handling.py`](FastAPI_Basics/error_handling.py)*

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

See: [`FastAPI_Basics/example.py`](FastAPI_Basics/example.py)

How to run (Windows PowerShell or CMD):
```bash
uvicorn example:app --reload
```


## 6. SQLAlchemy Async Example
This folder demonstrates integrating FastAPI with SQLAlchemy in async mode and a clean project layout (models, schemas, crud, routers, DB configuration). Below each file is explained: purpose, what it contains, and why key pieces (DATABASE_URL, engine, session, Base, get_db) are needed.

### .env
- Purpose: central place for environment configuration such as DATABASE_URL.
- Why: Keeps credentials and connection strings out of code, enables different configs per environment (development, CI, production) without changing source files.
- Utility: The app loads this file at startup to configure the async engine (connection string), so the same code can talk to SQLite locally or Postgres in production by changing the .env.

### [Database](SQLalchemy/app/database.py)
- Purpose: centralizes DB connection configuration, engine creation, session factory and Base metadata.
- What it contains:
  - Loading environment variables and reading DATABASE_URL.
  - Creating an async SQLAlchemy engine.
  - Creating an async_sessionmaker (SessionLocal) configured for request-scoped sessions.
  - Declaring Base = declarative_base() used by ORM models.
  - get_db() dependency that yields an async session using an async context manager.
- Why each concept exists and why it matters:
  - DATABASE_URL: a single connection string that tells SQLAlchemy which dialect/driver to use and how to connect (username, password, host, port, database). Changing this string is how you target different DBs.
  - Engine (create_async_engine): the engine is the central connection factory and pool manager. It prepares and manages connections, pooling and SQL execution behavior. Using an async engine enables non-blocking DB I/O when endpoints are async, improving concurrency.
  - echo=True (if present): logs SQL statements — invaluable during development to verify generated SQL and troubleshoot queries.
  - SessionLocal (async_sessionmaker): a factory for creating AsyncSession instances. Sessions are units of work — they keep track of ORM objects, pending changes and transaction boundaries. Using a sessionmaker centralizes session configuration (binding engine, expire_on_commit behavior).
  - expire_on_commit=False: prevents SQLAlchemy from expiring ORM object state on commit so returned objects remain usable after the transaction — convenient when returning ORM objects via FastAPI response models without an extra fetch.
  - Base = declarative_base(): a base class that model classes inherit from; it collects metadata (tables) so that schema creation and mapping work. Base.metadata is what create_all reads to create tables.
  - get_db() as an async dependency: yields a session per request using async with. The context manager ensures sessions are closed and connections returned to the pool automatically even on errors. This prevents leaked connections and keeps concurrency stable.
- How it interacts with other files:
  - Models inherit from Base so their table definitions are registered.
  - Routers/crud functions depend on get_db() to obtain an AsyncSession.
  - main.py uses the engine + Base.metadata to create tables at startup.

### [Models](SQLalchemy/app/models.py)
- Purpose: define the ORM model classes that map Python objects to DB tables and columns.
- What it contains:
  - One or more SQLAlchemy model classes (User, etc.) with Column definitions (types, primary key, constraints, indexes).
- Why models exist and what each choice means:
  - Model classes define schema and constraints in Python — SQLAlchemy uses them to generate SQL, perform queries, and produce ORM instances.
  - Primary keys identify rows uniquely and are required for ORM identity mapping.
  - Constraints like unique or index help enforce data integrity and improve query performance.
- How models are used:
  - CRUD functions use model classes for inserts and queries.
  - Pydantic schemas often map to/from model instances for request/response validation.

### [Schemas](SQLalchemy/app/schemas.py)
- Purpose: define Pydantic models (schemas) used for request validation and shaping API responses.
- What it contains:
  - Request models (e.g., UserCreate) with validation rules (min/max lengths, email type).
  - Response models (e.g., UserResponse) with orm_mode enabled.
- Why schemas are important:
  - They validate incoming payloads and ensure data conforms to expected types/constraints before hitting DB logic.
  - Response schemas document and control the outgoing JSON shape, preventing accidental leakage of internal fields (passwords, internal ids).
  - orm_mode allows Pydantic to read attributes from ORM objects directly (so returning an ORM instance works with response_model).
- How schemas interact with other pieces:
  - Routers declare request/response schemas which appear in OpenAPI docs.
  - CRUD functions accept and return objects compatible with these schemas (or raw ORM instances that Pydantic converts when orm_mode=True).

### [CRUD](SQLalchemy/app/crud.py)
- Purpose: implement the data access layer (repository) that encapsulates DB operations.
- What it contains:
  - Async functions that accept an AsyncSession and perform queries/inserts/updates/deletes using SQLAlchemy Core/ORM.
- Why separate CRUD logic:
  - Separation of concerns: keeps database logic out of HTTP route handlers, making code easier to test and reason about.
  - Reusability: the same CRUD functions can be used by multiple endpoints or background tasks.
  - Testing: CRUD functions can be unit-tested with a test DB/session independent of the web layer.
- Why AsyncSession and how it is used:
  - AsyncSession supports non-blocking DB operations; when used with an async engine and async endpoints, it avoids blocking the event loop.
  - CRUD functions use the session to add objects, commit transactions, refresh instances and execute async queries.
- Important patterns:
  - Use select(...) and execute(...) to query, then scalar_one_or_none() to get results.
  - Commit/refresh flow for new objects: add object, commit transaction, refresh to load generated DB fields (like id).

### [Users](SQLalchemy/app/routers/users.py)
- Purpose: define the HTTP routes (APIRouter) for user-related endpoints and wire them to the CRUD layer.
- What it contains:
  - Route handlers annotated with request and response schemas and dependency injection for DB sessions.
- Why use APIRouter and dependency injection:
  - APIRouter groups related endpoints for modularity and easier inclusion in the main app.
  - FastAPI's Depends(get_db) injects a session into handlers per request, ensuring proper lifecycle handling via the get_db context manager.
- How routers use schemas and CRUD:
  - Handlers accept validated Pydantic models (UserCreate), call CRUD functions with the AsyncSession, and return ORM objects; response_model controls output serialization.

### [main.py](SQLalchemy/app/main.py)
- Purpose: application entrypoint that assembles the FastAPI app, registers routers, and runs startup tasks.
- What it contains:
  - Creation of the FastAPI app instance.
  - A startup event that uses engine.begin() and Base.metadata.create_all to create tables.
  - Inclusion of routers (users and others).
  - A simple root health endpoint.
- Why create tables at startup:
  - Ensures DB schema exists during development/testing without manual migrations. In production you typically use managed migrations (Alembic) instead.
- Why use engine.begin() and run_sync(Base.metadata.create_all):
  - engine.begin() opens a transactional connection; run_sync is used to run synchronous metadata.create_all in the async engine context so tables are created safely when the app starts.


### launch.json
- Purpose: sample VS Code debug/run configuration for launching Uvicorn with the FastAPI app.
- What it configures:
  - Runs Uvicorn as a module with the import path to the FastAPI app.
  - Passes reload/host/port args.
  - Points to a workspace virtual environment python executable.
  - Loads environment variables from SQLalchemy/.env via envFile.
- Why useful:
  - Simplifies running and debugging the application from the IDE with proper env vars and interpreter.


## How the pieces fit together (end-to-end behavior)
1. At startup, main.py creates the FastAPI app and runs startup tasks. It uses the engine + Base metadata to create database tables if they don't exist (development convenience).
2. database.py created a configured async engine (connection pool) and a sessionmaker (SessionLocal). Models import Base so their table metadata is registered.
3. When a request arrives, a route defined in routers/users.py is invoked. The route declares a dependency on get_db() which yields an AsyncSession for the request using async with — this ensures the session is closed and the connection returned after request processing.
4. The route receives validated input via Pydantic schemas (schemas.py) and calls functions in crud.py, passing the AsyncSession. CRUD functions perform non-blocking DB operations via the async engine/session and commit/refresh as needed.
5. The route returns ORM objects or Pydantic response models. If response_model is used with orm_mode=True, Pydantic converts ORM objects to the declared JSON schema automatically.
6. Throughout development, logging (echo=True) and version diagnostics can help debug SQL and environment issues. The VS Code launch config and .env enable convenient local development.


### How to run:
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

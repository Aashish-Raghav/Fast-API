# Blog_Project — FastAPI + Async SQLAlchemy (JWT Auth)  

Concise, practical project demonstrating a production-oriented FastAPI app with:
- Async SQLAlchemy (aiosqlite for local testing)
- JWT authentication (access + refresh tokens)
- Clean separation: routers → crud → models → schemas → database
- Examples for users and posts with protected routes



## Quickstart (development)
1. Create and activate a virtual environment (Windows):
```bash
python -m venv .venv
Set-ExecutionPolicy RemoteSigned -Scope CurrentUser
.\venv_fastapi\Scripts\activate
Set-ExecutionPolicy Restricted -Scope CurrentUser  
```
2. From repository root install deps:
```bash
pip install -r requirement.txt  
```

3. Ensure env is present (app/.env or project .env). Example values:
```bash
DATABASE_URL=sqlite+aiosqlite:///./blog.db
SECRET_KEY=your_secret_here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=7
BCRYPT_ROUND=12
```
4. Run server (from project root):
```bash
cd Blog_Project
uvicorn app.main:app --reload
```
5. Open interactive docs:
```bash
Swagger UI: http://127.0.0.1:8000/docs
ReDoc: http://127.0.0.1:8000/redoc
```

## Environment & configuration
- Configuration is read using pydantic-settings (app.config.Settings) and uses env_file=".env" in `app/`.
- Key env vars:
  - DATABASE_URL — connection string (sqlite+aiosqlite:// or postgresql+asyncpg://user:pass@host/db)
  - SECRET_KEY, ALGORITHM — JWT signing settings
  - ACCESS_TOKEN_EXPIRE_MINUTES, REFRESH_TOKEN_EXPIRE_DAYS — token lifetimes
  - BCRYPT_ROUND — cost factor for bcrypt hashing


## Project layout (important files)
- app/main.py
  - FastAPI app factory, router registration and startup task that creates tables (development convenience).
- app/config.py
  - Centralized settings (Pydantic BaseSettings). Reads .env.
- app/database.py
  - Async DB configuration:
    - create_async_engine(settings.database_url, echo=True)
    - async_sessionmaker (SessionLocal) with expire_on_commit=False
    - Base = declarative_base()
    - get_db() dependency yields AsyncSession via `async with` (ensures cleanup)
  - Why these exist:
    - DATABASE_URL: single source for DB connection string
    - Engine: connection/pool manager used by sessions to run SQL
    - Session: unit-of-work for transactional DB access in a request
    - Base: registry for model metadata (used by create_all)
    - get_db: provides safe, request-scoped sessions and prevents leaked connections
- app/models.py
  - ORM models (User, Post). Defines columns, relationships and defaults.
  - Relationships (User.posts, Post.owner) allow convenient ORM navigation.
- app/schemas.py
  - Pydantic request/response models (validation & API shape). Response schemas use orm_mode where needed.
- app/crud.py
  - Async functions performing DB operations using AsyncSession (create, read, update, delete).
  - Keeps DB logic out of routers for testability and reuse.
- app/routers/
  - auth.py — register / login endpoints (issue JWTs)
  - users.py — protected user endpoints (me, list, get by id)
  - posts.py — CRUD for posts (protected create/update, public reads)
- app/auth/
  - jwt.py — create/verify access & refresh tokens (adds type, iat, expire claims)
  - utils.py — password hashing & verify (passlib / bcrypt)
  - dependencies.py — FastAPI dependency to resolve current user from Bearer token
- app/logger.py
  - App-level logger configuration (used across modules)


## API summary (endpoints)
```bash
Users (protected by JWT)
- POST /auth/register     — register a user
- POST /auth/login        — login (OAuth2 form) → returns access_token & refresh_token
- GET  /users/me          — current authenticated user
- GET  /users             — list users
- GET  /users/{id}        — get user by id

Posts
- POST   /posts           — create a post (requires auth; owner set from token)
- GET    /posts           — list posts
- GET    /posts/{id}      — get post
- GET    /posts/user/{id} — posts by user
- PATCH  /posts/{id}      — update (owner only)
- DELETE /posts/{id}      — update (owner only)
```

Notes:
- Authentication uses OAuth2 password flow: client posts credentials to `/auth/login` (form fields: username, password).
- Returned tokens: access_token (short-lived) and refresh_token (longer-lived).
- Protected routes use `OAuth2PasswordBearer` to extract Bearer token; token is verified by `app.auth.jwt.verify_token` and user resolved by `auth.dependencies.get_current_user`.


## JWT overview (how it's implemented here)
- Token contents: `sub` (subject/email), `user_id`, `type` ("access" or "refresh"), `iat`, `expire` (timestamp).
- create_access_token / create_refresh_token: add type and expiry and sign with SECRET_KEY using JOSE.
- verify_token: decodes, checks token type, and expiry; returns payload or None.
- get_current_user dependency:
  - extracts token via `OAuth2PasswordBearer`
  - verifies token and required payload fields
  - fetches user from DB and returns user instance or raises 401
- Why this pattern:
  - Keeps route handlers thin.
  - Centralizes token verification and user loading.
  - Supports access vs refresh tokens and safe expiry checks.


## Database notes & best practices
- Current development default: sqlite+aiosqlite for simplicity.
- For production use Postgres (postgresql+asyncpg) and enable connection pooling and proper connection limits.
- Use Alembic for migrations (do not rely on create_all in production).
- Keep SECRET_KEY secure (use environment or secret manager).

## Testing & debugging
- Use FastAPI's TestClient for unit/integration tests; create a test DB URL for CI.
- Enable `echo=True` in create_async_engine for SQL logs during development.
- VS Code: you can add a launch configuration to run uvicorn and point envFile to `app/.env`.

## Next steps / improvements
- Replace create_all with Alembic migrations.
- Add refresh token rotation and blacklisting support.
- Improve tests (unit + integration with test DB).
- Add role-based access control and rate limiting.
- Add pagination, filtering and search for posts.
- Dockerize and add CI/CD.

## Resources
- FastAPI docs: https://fastapi.tiangolo.com  
- SQLAlchemy async: https://docs.sqlalchemy.org/en/20/orm/extensions/asyncio.html  
- JOSE (python-jose): https://python-jose.readthedocs.io

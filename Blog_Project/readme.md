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

## Testing

This project includes an async test suite using pytest, pytest-asyncio and httpx. Tests run against an in-memory SQLite database and override the app's get_db dependency so tests are isolated from your development database.

What is tested now
- Authentication flows (tests/test_auth.py)
  - Registration success and duplicate registration handling
  - Validation (invalid email, short password)
  - Login success, wrong password, non-existent user, and missing credentials
- Test fixtures provide reusable setup:
  - db_session: creates and tears down an in-memory DB per test
  - client: httpx AsyncClient bound to the FastAPI app with dependency override
  - test_user / test_user_2: pre-created users for tests
  - auth_headers: obtains a Bearer token for authenticated requests
  - test_post: example post linked to a test user

How tests work (brief)
- Tests use create_async_engine with sqlite+aiosqlite:///:memory: to create a transient test DB.
- Base.metadata.create_all() is run at fixture setup and dropped afterwards.
- app.dependency_overrides[get_db] is used to inject the test DB session into route handlers.
- httpx.AsyncClient (ASGITransport) runs requests against the application without network I/O.

Run tests (development)
- Install test dependencies (if not already installed):
  - pytest, pytest-asyncio, httpx
- From project root:
```bash
pip install -r requirement.txt
pytest -q
```
- Run a single test file:
```bash
pytest tests/test_auth.py -q
```
- Run a single test by node id:
```bash
pytest tests/test_auth.py::TestAuthEndpoints::test_login -q
```

Notes and troubleshooting
- If tests cannot import settings or .env values, ensure your environment and pythonpath are set correctly when running pytest.
- Tests rely on async fixtures; use pytest-asyncio plugin (installed via requirements).
- The in-memory SQLite engine used in tests may behave differently from a persistent DB (e.g., concurrency or foreign-key behaviors). Use an ephemeral file-based SQLite or a test Postgres instance for higher fidelity integration tests.

Further tests to add (planned)
- Full posts CRUD test coverage (create/read/update/delete + ownership checks)
- Protected route access tests for token expiry and invalid tokens
- Edge cases and validation tests for input schemas
- Integration tests with a file-based test DB or test Postgres
- Tests for auth refresh token flow and logout/blacklist logic
- End-to-end tests including migrations (Alembic) and startup scripts

CI / Coverage
- Add a CI workflow (GitHub Actions) to run pytest, run linters and collect coverage reports.
- Consider running tests in a matrix for multiple Python versions and database backends.

If you want, I can:
- Add a GitHub Actions workflow file for running tests.
- Provide example pytest commands or fix the requirements file for missing test deps.

## Advanced testing internals & notes

This section explains low-level behavior that affects async tests, dependency overrides and DB connection lifetimes.

1) How TestClient / httpx run the app (threads vs event loop)
- Starlette / FastAPI TestClient (sync) runs the ASGI app in a background thread and drives it with a requests-like interface. The app runs on an event loop created inside that thread.
- httpx.AsyncClient with ASGITransport (used in async tests) calls the ASGI app directly without real network I/O and is designed to run inside an async test function's event loop.
- Practical implication: choose the client that matches your test style. Sync TestClient isolates the app in a thread; httpx.AsyncClient keeps everything in the test's async loop.

2) How dependency overrides interact with async loops
- app.dependency_overrides simply replaces the dependency callables used by FastAPI when resolving dependencies.
- If the test harness runs the app in a different thread/loop (sync TestClient), overrides must not capture or depend on the test function's event loop or objects tied to the main loop.
- For async tests with httpx.AsyncClient, overrides may be async and can yield AsyncSession objects created in the same loop. This is the safest approach for async DB sessions.
- Rule of thumb: create engine/sessions and yield them in the same loop where the request handling runs (or use lazy session creation inside override).

3) Running async tests without pytest-asyncio
Options:
- pytest-anyio: add pytest-anyio and mark tests with @pytest.mark.anyio to run async tests with anyio backend (recommended alternative).
- Use asyncio.run(...) inside a synchronous test to run a coroutine (quick hack, not ideal for many tests).
- Use httpx.AsyncClient in combination with an event loop fixture you control (for manual loop management).
- Best practice: use pytest-asyncio or pytest-anyio for clear async fixture integration.

4) How SQLAlchemy async drivers bind connections to event loops
- Async DB drivers (aiosqlite, asyncpg) create connections tied to the event loop where they were instantiated.
- If a connection is opened in loop A and subsequently used in loop B (e.g., app running in a different test thread), the driver may raise errors or behave incorrectly.
- To avoid this:
  - Create engines/sessions in the same loop that will use them, or
  - Use a session factory override that creates sessions lazily inside the request handler loop, or
  - For tests, create the engine and run create_all in the test loop and provide that session via dependency override.

5) Why Uvicorn threadpools / workers differ from TestClient
- Uvicorn (production/dev server) runs an asyncio event loop per process (or per worker) and may use threadpools to run blocking code (via loop.run_in_executor). It accepts real network connections.
- TestClient / httpx ASGITransport do not emulate external network conditions and often run the app inside the test process / thread. They do not create network sockets and therefore do not exercise process/worker-level behavior (connection pooling across workers).
- Consequence: some concurrency bugs or loop-binding issues only surface under Uvicorn/Gunicorn (multiple workers, real network), not in TestClient. Always validate critical concurrency behavior in an environment closer to production (e.g., running Uvicorn locally or in CI).

Practical checklist for reliable async tests
- Use async-compatible test client (httpx.AsyncClient + ASGITransport) for async tests.
- Create test engine and sessions inside the same async loop used by tests.
- Override get_db with an async generator that yields the test AsyncSession.
- Avoid sharing connections across loops; prefer session-per-request pattern via get_db.
- Run a small integration run with uvicorn (or a worker setup) to catch production-only issues.


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

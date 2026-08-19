# Task Manager API

This is a backend task-management API I built with **FastAPI**, **PostgreSQL**, **Redis**, **JWT authentication**, **Docker**, and **pytest**.

 I created this project to learn FastAPI, strengthen my programming skills, and gain practical experience with backend development. The project includes Redis caching and cache invalidation, task search and filtering, pagination, automated API testing with pytest, and Docker-based containerization for reproducible environments.

## Features

- User registration and login with JWT authentication
- Password hashing using Argon2
- Protected API endpoints
- User-specific task authorization and ownership checks
- Full task CRUD operations
- Task search, filtering, sorting, and pagination
- PostgreSQL persistence with database health checks
- Redis caching with cache hits, misses, and cache invalidation
- Automated API and integration testing with pytest
- Separate test database and test Redis environment
- Environment-based configuration using `.env`
- Docker and Docker Compose containerization
- Service health checks and dependency-aware startup

## Tech Stack

- Python 3.13
- FastAPI
- Uvicorn
- Pydantic
- PostgreSQL 17
- Redis 7
- Psycopg 3
- JWT (`python-jose`)
- Argon2 (`pwdlib` / `argon2-cffi`)
- pytest + TestClient
- Docker + Docker Compose

## Project Structure

```text
Taskmanager/
├── app.py
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── .env.example
├── .gitignore
├── .dockerignore
├── conftest.py
│
├── Database/
│   ├── init.sql
│   ├── sql_config.py
│   ├── connection.py
│   ├── redis_config.py
│   └── redis_connection.py
│
├── repositories/
├── services/
├── routers/
├── schemas/
└── tests/
```

> The exact module names may vary slightly as the project evolves; the important separation is between app > routers > services > repositories, schemas, and database/config code.

## Architecture

```text
                Client
                  │
                  ▼
             FastAPI / API
                  │
          ┌───────┴────────┐
          │                │
          ▼                ▼
      Services         Authentication
          │                │
      ┌───┴────┐           │
      ▼        ▼           ▼
 PostgreSQL   Redis      JWT
      │        │
      └────────┘
```

For task searches, the service uses a cache-aside flow:

```text
GET /tasks
   │
   ▼
Redis GET
   │
   ├── HIT  ──► return cached result
   │
   └── MISS ──► PostgreSQL
                  │
                  ▼
               Redis SET
                  │
                  ▼
               return
```

When tasks r created, updated, or deleted, the affected user's task-cache entries are invalidated and deleted so stale/old search results are not served to control redundancy.

## Running with Docker

### 1. Configure environment variables

Create a local `.env` file from `.env.example`.

Example:

```env
SECRET_KEY=replace-me
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

DB_NAME=python_backend
DB_USER=postgres
DB_PASSWORD=replace-me
DB_HOST=postgres
DB_PORT=5432

REDIS_HOST=redis
REDIS_PORT=6379
REDIS_DECODE_RESPONSE=true
REDIS_TTL=500
```


### 2. Start the stack

```bash
docker compose up -d --build
```

This starts:

- FastAPI
- PostgreSQL
- Redis

and creates the Docker network and PostgreSQL volume.

### 3. Check services

```bash
docker compose ps
```

The PostgreSQL and Redis services should report healthy status.

### 4. Open the API docs

Open:

```text
http://localhost:8000/docs
```

The interactive Swagger UI can be used to register, log in, authenticate, and test task endpoints.

### 5. Stop the stack

```bash
docker compose down
```

To remove the PostgreSQL Docker volume as well:

```bash
docker compose down -v
```

> `-v` deletes the Docker database volume. Use it intentionally.

## Running Tests

The test suite uses a separate PostgreSQL database and a host-side Redis connection so tests do not use the normal development database.

Run:

```bash
pytest -vv -s
```

The suite covers:

- registration and validation
- duplicate registration
- authentication
- protected endpoints
- task creation, search, update, and deletion
- user/task ownership isolation
- Redis cache hits
- Redis cache invalidation

The test environment is configured in `conftest.py`.

## Environment Notes

The application uses different hosts depending on where it runs:

```text
Inside Docker:
PostgreSQL → postgres:5432
Redis      → redis:6379

Windows test runner:
PostgreSQL → 127.0.0.1:5433
Redis      → 127.0.0.1:6380
```

This is intentional: `postgres` and `redis` are Docker Compose service names and are resolvable from containers, while pytest running on Windows connects through published host ports.

## API Behavior

Typical task operations include:

```text
POST   /register
POST   /login
GET    /me

POST   /task
GET    /tasks
GET    /tasks/{id}
PUT    /task/{id}
DELETE /task/{id}
```

Task search supports filtering and pagination through query parameters.

Authentication uses a bearer JWT, and task access is restricted by `user_id`, preventing one user from reading, updating, or deleting another user's tasks.

## Security Notes

- Passwords are hashed before storage.
- JWT secrets are loaded from environment variables.
- `.env` is excluded from Git.
- API responses do not expose stored passwords.
- Task queries include ownership checks.

Before publishing or deploying:

1. Replace any development JWT secret with a newly generated secret.
2. Use strong, unique database credentials.
3. Keep `.env` out of source control.
4. Review exposed ports and deployment settings for your target environment.

## Development

Create/activate the virtual environment, install dependencies, and run FastAPI locally:

```bash
pip install -r requirements.txt
uvicorn app:app --reload
```

For the reproducible multi-service environment, Docker Compose is recommended.

## Project Status

The backend currently includes the core API, authentication, authorization, PostgreSQL persistence, Redis caching, Docker Compose, and automated tests. 

## Dev notes
While making this project Ive learned alot about backend i'll keep making more projects and keep learning.

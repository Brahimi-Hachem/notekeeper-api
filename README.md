# NoteKeeper API

NoteKeeper API is a production-oriented FastAPI backend for personal notes and user-scoped knowledge storage. It includes authentication, PostgreSQL persistence, SQLAlchemy 2.x models, Alembic migrations, Docker Compose development, and automated tests.

> The Streamlit UI has been moved to a separate repository: `notekeeper-ui`.

## Features

- User registration and login
- JWT-based authentication
- User-scoped notes: create, list, retrieve, update, delete
- PostgreSQL persistence with SQLAlchemy
- Alembic migrations for schema management
- Local Docker Compose development stack
- Automated tests with pytest
- Ruff linting and formatting

## Tech stack

- Python 3.12
- FastAPI
- Uvicorn
- SQLAlchemy 2.x
- Alembic
- PostgreSQL
- PyJWT
- pwdlib for password hashing
- pytest, FastAPI TestClient
- Docker and Docker Compose
- Ruff

## Repository layout

```text
notekeeper-api/
├── app/
│   ├── api/
│   │   └── routers/
│   ├── core/
│   ├── db/
│   │   ├── models/
│   │   ├── base.py
│   │   └── session.py
│   ├── schemas/
│   └── main.py
├── alembic/
├── docs/
├── tests/
├── Dockerfile
├── docker-compose.yml
├── docker-entrypoint.sh
├── pyproject.toml
├── .env.example
└── README.md
```

## Getting started

### Prerequisites

- Python 3.12
- PostgreSQL for local development
- Docker and Docker Compose for containerized development

### Local development

1. Copy `.env.example` to `.env`.
2. Update `DATABASE_URL` to point at a local PostgreSQL instance.
3. Apply the database schema with Alembic:

```cmd
uv run alembic upgrade head
```

4. Start the app:

```cmd
uv run uvicorn app.main:app --reload
```

5. Open the API docs at:

- http://127.0.0.1:8000/docs

### Docker development

1. Copy `.env.example` to `.env`.
2. Build and start the services:

```cmd
docker compose up --build
```

3. The API will be available at:

- http://127.0.0.1:8000
- http://127.0.0.1:8000/docs

The `web` container waits for PostgreSQL and runs Alembic migrations automatically before starting the FastAPI server.

> The Streamlit UI has been moved to a separate repository: `notekeeper-ui`.

### Environment variables

- `DATABASE_URL` – SQLAlchemy connection string for PostgreSQL
- `JWT_SECRET_KEY` – secret key used to sign JWTs
- `JWT_ALGORITHM` – JWT signing algorithm
- `ACCESS_TOKEN_EXPIRE_MINUTES` – token expiration time

## Database migrations

Create or update the schema with Alembic:

```cmd
uv run alembic revision --autogenerate -m "describe change"
uv run alembic upgrade head
```

To roll back the most recent migration:

```cmd
uv run alembic downgrade -1
```

## Testing

Run the test suite:

```cmd
uv run pytest
```

Run Ruff linting and formatting checks:

```cmd
uv run ruff check .
uv run ruff format .
```

## Phase roadmap

- Phase 04: Alembic migrations and versioned schema management ✅
- Phase 05: Docker Compose local development ✅
- Phase 06: GitHub Actions CI/CD and deployment 🚧
- Phase 07: Streamlit web interface prototype 🚧

## Notes

- Docker Compose maps the db container port `5432` to host `5433`.
- The local development path uses the `.env` file to configure the application.
- Use `docker compose down` when you want to stop and remove the development containers.

## Next steps

After documentation and Docker setup, the next phase will add GitHub Actions for CI and GitHub integration. Then the project will move to deployment and later a Streamlit test interface.

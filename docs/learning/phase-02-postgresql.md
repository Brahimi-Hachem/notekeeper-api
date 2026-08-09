# Phase 02 — PostgreSQL database integration

## Why PostgreSQL

The API now stores notes in PostgreSQL rather than returning hard-coded data.
PostgreSQL provides durable relational storage, database constraints, and a
clear path to migrations in a later phase.

## Local Docker setup

PostgreSQL 17 runs as the `postgres` service in `docker-compose.yml`. It uses
the `notekeeper` database and role, and persists its data in the named
`postgres_data` Docker volume. The host port is `5433`, mapped to PostgreSQL's
container port `5432`, because port `5432` on this Windows machine was already
served by a different PostgreSQL instance.

The application configuration in `.env` uses:

```text
postgresql+psycopg://notekeeper:notekeeper_dev@127.0.0.1:5433/notekeeper
```

## SQLAlchemy components

`app/db/session.py` creates the SQLAlchemy engine, the `SessionLocal`
sessionmaker, and the `get_db()` FastAPI dependency. Each request receives a
session and the dependency closes it in a `finally` block.

`app/db/base.py` defines the declarative `Base`. ORM models inherit from it.
`app/db/models/note.py` maps the `Note` model to the `notes` table:

- `id`: integer primary key
- `title`: non-null string, limited to 200 characters
- `content`: non-null text
- `created_at`: non-null, timezone-aware database timestamp
- `updated_at`: non-null, timezone-aware database timestamp, refreshed on ORM
  updates where supported by the database

`app/db/init_db.py` imports the models before calling `Base.metadata.create_all`.
The application calls `init_db()` during FastAPI startup, which creates the
development table when it does not yet exist. This is a development-only
initialization approach; Alembic migrations are intentionally deferred to a
later phase.

## ORM models, schemas, and tables

The database table stores rows. The SQLAlchemy `Note` ORM model maps Python
objects to those rows. Pydantic `NoteCreate` and `NoteResponse` schemas define
the HTTP request and response contract. `NoteResponse` uses Pydantic v2
`from_attributes` support so it can serialize the returned ORM object without
exposing timestamp fields that are not yet part of the API contract.

## CRUD implemented so far

`POST /notes/` validates a `NoteCreate` request, adds an ORM model to the
session, commits it, refreshes its database-generated values, and returns the
persisted note with HTTP 201.

`GET /notes/` reads notes from PostgreSQL and returns them ordered by ID. It
returns an empty list when no notes exist.

## Tests and isolation

The Notes tests use a separate `notekeeper_test` PostgreSQL database by
default. It is created automatically when absent. Set `TEST_DATABASE_URL` to
use a different dedicated test database. For each test, an outer transaction
and overridden FastAPI `get_db` dependency ensure endpoint commits are rolled
back afterward. This avoids deleting or depending on a developer's existing
records while still testing the SQLAlchemy/PostgreSQL integration.

## Useful verification commands

```powershell
docker compose ps
docker compose exec postgres sh -lc "PGPASSWORD=notekeeper_dev psql -h 127.0.0.1 -U notekeeper -d notekeeper -c 'SELECT current_user, current_database();'"
uv run python -c "from sqlalchemy import text; from app.db.session import engine; print(engine.connect().execute(text('SELECT 1')).scalar())"
docker compose exec postgres psql -U notekeeper -d notekeeper -c "\\dt notes"
uv run ruff check .
uv run ruff format --check .
uv run pytest -v
```

## Debugging note

The container accepted the configured credentials, but a Windows-hosted
connection to port `5432` failed authentication and did not appear in the
container logs. That showed `5432` was a different local PostgreSQL server.
Changing the Docker host mapping and application URL to `5433` directed the
API to the intended container without deleting `postgres_data`.

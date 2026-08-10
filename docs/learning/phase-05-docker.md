# Phase 05 — Dockerized Local Development

## Goal
Make the entire backend stack reproducible using Docker and Docker Compose.

## How to use it

1. Build and start the services:

```bash
docker compose up --build
```

2. Open the API:

- http://127.0.0.1:8000
- Swagger docs: http://127.0.0.1:8000/docs

## Services

- `web` — FastAPI application
- `postgres` — PostgreSQL database

## Environment

Configure service environment variables in `.env` or `.env.example`.

## Notes

- The web service waits for PostgreSQL before starting.
- Database schema should be managed via Alembic migrations.

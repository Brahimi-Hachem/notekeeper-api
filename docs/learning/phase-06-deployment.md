# Phase 06 — Deployment

## Goal
Deploy the NoteKeeper API to a free hosting provider so the backend is accessible publicly.

## Recommended provider

The simplest free deployment path for this project is Render.com using Docker.
Render supports GitHub-connected deployments and can run the existing `Dockerfile` and `docker-entrypoint.sh`.

## Deployment approach

### 1. Connect GitHub

1. Sign in to Render with GitHub.
2. Connect the `Brahimi-Hachem/notekeeper-api` repository.

### 2. Create a PostgreSQL database

If Render still offers a free PostgreSQL plan, create a managed database named `notekeeper`.
If free managed Postgres is not available, use any free PostgreSQL service and set its connection URL.

### 3. Create the web service

1. Create a new Web Service.
2. Choose `Docker` as the environment.
3. Set the branch to `main`.
4. Set `DockerfilePath` to `Dockerfile`.
5. Add environment variables:
   - `DATABASE_URL` — the connection string for the database
   - `JWT_SECRET_KEY` — a long random secret
   - `JWT_ALGORITHM` — `HS256`
   - `ACCESS_TOKEN_EXPIRE_MINUTES` — `30`

### 4. Deployment behavior

The app already includes a Docker entrypoint that:

- waits for PostgreSQL to become available,
- runs `uv run alembic upgrade head` to apply migrations,
- starts Uvicorn on port `8000`.

This means the deployed service can bootstrap the schema automatically.

## Render manifest

A `render.yaml` manifest has been added to the repository. It can be used by Render to define the web service and database from the repo.

## Free tier considerations

- Free instances may sleep when idle.
- Cold starts can be slower.
- The API may need an external database if managed free databases are not available.

## Verification

After deployment, verify the API using the deployed URL:

- `https://<service-name>.onrender.com/docs`

Then test:

- `POST /auth/register`
- `POST /auth/login`
- `POST /notes/`
- `GET /notes/`

## Next step

After the backend is deployed, Phase 07 will add a frontend experience. The first option is a lightweight Streamlit UI, then optionally a Telegram or WhatsApp conversational interface.

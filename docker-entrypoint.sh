#!/bin/sh
set -e

if [ -z "$DATABASE_URL" ]; then
    echo 'ERROR: DATABASE_URL is not set.'
    exit 1
fi

echo 'Waiting for database to be available...'

until python -c "from sqlalchemy import create_engine; import os; engine=create_engine(os.environ['DATABASE_URL']); engine.connect(); print('db ok')"; do
    echo "Database connection failed. Retrying..."
    sleep 2
done

echo 'Applying database migrations...'
uv run alembic upgrade head

echo 'Starting Uvicorn...'
exec uv run uvicorn app.main:app --host 0.0.0.0 --port "$PORT"

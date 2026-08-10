import os
from collections.abc import Generator

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import Engine, create_engine, text
from sqlalchemy.engine import URL, make_url
from sqlalchemy.orm import Session, sessionmaker

from app.core.config import settings
from app.db.base import Base
from app.db.models import Note, User
from app.db.session import get_db
from app.main import app


def get_test_database_url() -> URL:
    configured_url = os.getenv("TEST_DATABASE_URL")
    if configured_url:
        return make_url(configured_url)

    application_url = make_url(settings.database_url)
    database_name = application_url.database
    if database_name is None:
        raise RuntimeError("DATABASE_URL must include a database name.")
    return application_url.set(database=f"{database_name}_test")


def create_test_database(database_url: URL) -> None:
    database_name = database_url.database
    if database_name is None or not database_name.replace("_", "").isalnum():
        raise RuntimeError(
            "The test database name must contain only letters, numbers, and "
            "underscores."
        )

    admin_engine = create_engine(
        database_url.set(database="postgres"),
        isolation_level="AUTOCOMMIT",
    )
    with admin_engine.connect() as connection:
        database_exists = connection.scalar(
            text("SELECT 1 FROM pg_database WHERE datname = :database_name"),
            {"database_name": database_name},
        )
        if database_exists is None:
            connection.execute(text(f'CREATE DATABASE "{database_name}"'))
    admin_engine.dispose()


@pytest.fixture(scope="session")
def test_engine() -> Generator[Engine, None, None]:
    database_url = get_test_database_url()
    create_test_database(database_url)
    engine = create_engine(database_url, pool_pre_ping=True)

    Base.metadata.create_all(
        bind=engine,
        tables=[User.__table__, Note.__table__],
    )

    yield engine
    engine.dispose()


@pytest.fixture
def client(test_engine: Engine) -> Generator[TestClient, None, None]:
    connection = test_engine.connect()
    transaction = connection.begin()
    test_session = sessionmaker(bind=connection, class_=Session)()

    def override_get_db() -> Generator[Session, None, None]:
        yield test_session

    app.dependency_overrides[get_db] = override_get_db

    with TestClient(app) as test_client:
        yield test_client

    app.dependency_overrides.pop(get_db)
    test_session.close()
    transaction.rollback()
    connection.close()


@pytest.fixture
def auth_headers(client: TestClient) -> dict[str, str]:
    register_response = client.post(
        "/auth/register",
        json={
            "email": "test@example.com",
            "password": "password123",
        },
    )

    assert register_response.status_code == 201

    login_response = client.post(
        "/auth/login",
        json={
            "email": "test@example.com",
            "password": "password123",
        },
    )

    assert login_response.status_code == 200

    token = login_response.json()["access_token"]

    return {"Authorization": f"Bearer {token}"}

# Phase 1 — FastAPI Foundation

## Goals

- Understand what FastAPI is
- Understand REST APIs
- Understand HTTP methods and status codes
- Build the application entrypoint
- Understand FastAPI routers
- Understand Pydantic schemas
- Separate API, service, and repository responsibilities
- Write the first API tests
- Understand how the application is started
- Build a health-check endpoint

---

# FastAPI

FastAPI is a Python web framework for building APIs.

It provides:

- HTTP routing
- request validation
- response validation
- automatic OpenAPI documentation
- dependency injection
- asynchronous support

---

# REST API

A REST API exposes resources through HTTP.

Example resource:

    notes

Typical operations:

    GET    /notes
    GET    /notes/{id}
    POST   /notes
    PATCH  /notes/{id}
    DELETE /notes/{id}

---

# HTTP Methods

GET
    Retrieve data.

POST
    Create a resource.

PUT
    Replace a resource.

PATCH
    Partially update a resource.

DELETE
    Delete a resource.

---

# HTTP Status Codes

200
    Successful request.

201
    Resource created.

204
    Successful request with no response body.

400
    Bad request.

401
    Authentication required/failed.

403
    Authenticated but not authorized.

404
    Resource not found.

422
    Request validation failed.

500
    Unexpected server error.

---

# Pydantic

Pydantic validates and parses Python data.

FastAPI uses Pydantic for request and response schemas.

Conceptually:

    HTTP JSON
        ↓
    Pydantic schema
        ↓
    validated Python data
        ↓
    application logic

---

# Application Architecture

API layer
    Handles HTTP requests and responses.

Service layer
    Contains business logic.

Repository layer
    Handles data access.

The goal is to avoid putting all application logic inside route functions.

---

# Health Endpoint

The health endpoint is used to determine whether the API process is running.

Example:

    GET /health

Expected response:

    {
        "status": "ok"
    }
# HTTP and REST Fundamentals

## HTTP Request

A request contains:

    HTTP method
    URL
    headers
    optional body

Example:

    POST /notes

    Content-Type: application/json

    {
        "title": "Learning FastAPI",
        "content": "..."
    }

## HTTP Response

A response contains:

    status code
    headers
    optional body

Example:

    201 Created

    {
        "id": 1,
        "title": "Learning FastAPI"
    }


## REST Resources

REST APIs model resources.

Instead of:

    /createNote
    /deleteNote
    /getNotes

Prefer:

    POST   /notes
    DELETE /notes/{note_id}
    GET    /notes


## Path Parameters

Example:

    GET /notes/42

Route:

    /notes/{note_id}

The value 42 is a path parameter.


## Query Parameters

Example:

    GET /notes?tag=python&limit=10

Query parameters:

    tag=python
    limit=10


## Request Body

Example:

    POST /notes

    {
        "title": "Learning FastAPI",
        "content": "..."
    }

The request body contains the data sent to the API.


## Important Status Codes

200
    Successful request.

201
    Resource created.

204
    Successful request with no body.

400
    Bad request.

401
    Authentication required or failed.

403
    Authenticated but not authorized.

404
    Resource not found.

422
    Request validation failed.

500
    Unexpected server error.



    # Pydantic Schemas

Pydantic schemas define the data contracts of the API.

They validate and parse incoming/outgoing data.

Conceptually:

    JSON request
        ↓
    Pydantic schema
        ↓
    validated Python data
        ↓
    application logic


## Request Schema

A request schema defines what the client may send.

Example:

    class NoteCreate(BaseModel):
        title: str
        content: str


## Response Schema

A response schema defines what the API returns.

Example:

    class NoteResponse(BaseModel):
        id: int
        title: str
        content: str


## Why separate request and response schemas?

Input and output are different contracts.

Example:

    NoteCreate

    {
        "title": "...",
        "content": "..."
    }

while:

    NoteResponse

    {
        "id": 1,
        "title": "...",
        "content": "..."
    }


## Field Validation

Pydantic's Field can define constraints.

Example:

    title: str = Field(min_length=1, max_length=200)

This prevents invalid input from reaching the business logic.


# API Testing with Pytest

FastAPI provides TestClient for testing API endpoints without starting
a real HTTP server.

Example:

    from fastapi.testclient import TestClient

    from app.main import app

    client = TestClient(app)


## Basic API Test

    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


## Testing Request Validation

Invalid requests should also be tested.

Example:

    response = client.post(
        "/notes/",
        json={
            "title": "",
            "content": "test",
        },
    )

    assert response.status_code == 422


## Test Principle

Test observable behavior rather than implementation details.

Example:

    Good:
        assert the API returns 422 for invalid input.

    Less useful:
        test exactly how Pydantic internally performs validation.


## TestClient

TestClient allows API tests without manually starting Uvicorn.

Normal application:

    Client
        ↓
    Uvicorn
        ↓
    FastAPI


Test:

    TestClient
        ↓
    FastAPI




## Testing & Code Quality — Key Lessons
### Pytest

Pytest discovers test files and test functions according to naming conventions.

Typical structure:

tests/
    test_health.py
    test_notes.py

Typical test function:

def test_something():
    ...

Run tests:

    uv run pytest

Verbose:

    uv run pytest -v


### TestClient

FastAPI's TestClient allows us to test API endpoints without manually
starting the production server.

Example:

    client = TestClient(app)

    response = client.get("/health")


### Assertions

Tests verify expected behavior.

Example:

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


### Validation Testing

Invalid input should be tested explicitly.

Example:

    {
        "title": "",
        "content": "test"
    }

Pydantic rejects invalid input before the endpoint's business logic
should execute.

For FastAPI validation failures, the typical HTTP status is:

    422 Unprocessable Entity


### Ruff

Ruff provides:

    ruff check .
        → linting

    ruff check --fix .
        → automatically fix supported lint issues

    ruff format .
        → format Python files

    ruff format --check .
        → verify formatting without modifying files


### pre-commit

pre-commit runs configured checks before a Git commit.

Install hooks:

    uv run pre-commit install

Run manually:

    uv run pre-commit run --all-files

Our current hooks:

    Ruff lint
    Ruff format

Important distinction:

    pre-commit
        = local quality gate

    GitHub Actions
        = remote CI quality gate


### Test Pyramid

We will eventually have:

    Unit tests
        ↓
    Service/repository tests
        ↓
    API/integration tests
        ↓
    End-to-end tests

The project will gradually introduce these as the architecture becomes
more sophisticated.



## Application Configuration

Never hard-code environment-specific configuration or secrets
inside application source code.

Use environment variables.

Local:
    .env

Repository:
    .env.example

Production:
    platform/environment secrets

Flow:

    Environment
        ↓
    Pydantic Settings
        ↓
    Application
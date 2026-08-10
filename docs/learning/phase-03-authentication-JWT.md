# Phase 03 — Authentication & Authorization

## Overview

Phase 03 adds authentication and user-scoped authorization to the NoteKeeper API.

The goal was to move from an API where notes could be accessed without a user identity to an API where:

- Users can register accounts.
- Users can log in securely.
- Passwords are hashed before being stored.
- Successful login returns a JWT access token.
- Protected endpoints require a valid JWT.
- The authenticated user is available through FastAPI dependencies.
- Notes belong to a specific user.
- Users can only access their own notes.

This phase establishes the authentication foundation required for a multi-user application.

---

# 1. Authentication Architecture

The authentication flow is:

1. User registers with an email and password.
2. The password is validated and hashed.
3. The user is stored in PostgreSQL.
4. User logs in with email and password.
5. The stored password hash is verified.
6. A JWT access token is generated.
7. The client sends the token with protected requests.
8. FastAPI extracts and validates the token.
9. The authenticated user is resolved from the database.
10. Protected endpoints use the authenticated user to enforce ownership.

The important separation is:

- **Authentication** → Who is the user?
- **Authorization** → Is this user allowed to access this resource?

---

# 2. User Model

The `User` SQLAlchemy model represents an authenticated application user.

The model contains:

- `id`
- `email`
- `hashed_password`
- `created_at`

The database stores the password hash, never the original password.

This is important because passwords should never be persisted as plaintext.

---

# 3. Password Hashing

Passwords are hashed before being stored in the database.

The authentication service is responsible for:

- hashing passwords during registration
- verifying passwords during login

Conceptually:

    plaintext password
            ↓
       password hash
            ↓
       PostgreSQL

During login:

    submitted password
            ↓
       verification
            ↓
    stored password hash
            ↓
       authentication

The application never needs to recover the original password.

---

# 4. User Registration

Endpoint:

    POST /auth/register

Request:

    {
        "email": "user@example.com",
        "password": "password123"
    }

The registration flow:

1. Validate the request using Pydantic.
2. Check whether the email already exists.
3. Reject duplicate emails.
4. Hash the password.
5. Create the user.
6. Commit the user to the database.
7. Return the public user representation.

A successful registration returns HTTP `201 Created`.

The response does not expose the password or password hash.

---

# 5. User Login

Endpoint:

    POST /auth/login

Request:

    {
        "email": "user@example.com",
        "password": "password123"
    }

The login flow:

1. Find the user by email.
2. Verify the supplied password against the stored hash.
3. Reject invalid credentials.
4. Generate a JWT access token.
5. Return the token to the client.

Successful authentication returns:

    {
        "access_token": "...",
        "token_type": "bearer"
    }

The token contains the user's ID as its subject.

---

# 6. JWT Authentication

JWT is used to represent an authenticated session without storing session state on the server.

The token contains information such as:

- `sub` — the authenticated user's ID
- `exp` — token expiration time

The API currently creates access tokens with a limited lifetime.

The client sends the token using the HTTP Authorization header:

    Authorization: Bearer <access_token>

The authentication dependency extracts this token and validates it before allowing access to protected endpoints.

---

# 7. FastAPI Dependencies

Authentication is implemented using FastAPI's dependency injection system.

The application defines a dependency responsible for resolving the current user.

Conceptually:

    request
       ↓
    Authorization header
       ↓
    JWT validation
       ↓
    user ID
       ↓
    database lookup
       ↓
    current user

Protected routes can then declare the current user as a dependency instead of implementing authentication logic themselves.

This keeps authentication logic centralized and reusable.

---

# 8. Current User Dependency

Protected routes use a dependency similar to:

    CurrentUser = Annotated[
        User,
        Depends(get_current_user),
    ]

This allows endpoints to receive the authenticated user directly.

For example, note operations can use:

    current_user.id

to determine which user's notes should be accessed.

This is preferable to accepting a `user_id` from the request because the client should not be trusted to decide which user it represents.

---

# 9. User-Scoped Notes

Notes were updated to belong to a specific user.

The `notes` table contains:

    user_id

This creates the relationship:

    User
      │
      └──< Notes

One user can own many notes.

Each note belongs to exactly one user.

When creating a note, the application uses the authenticated user:

    Note(
        ...,
        user_id=current_user.id,
    )

The user ID therefore comes from the verified JWT rather than from the request body.

---

# 10. Authorization

Authentication alone is not enough.

A user may have a valid token but still must not be allowed to access another user's notes.

Queries therefore filter by both:

    Note.id == note_id

and:

    Note.user_id == current_user.id

For list operations, the query is scoped to:

    Note.user_id == current_user.id

This guarantees that a user only receives their own notes.

---

# 11. Protected Note Operations

The following endpoints require authentication:

    GET    /notes/
    POST   /notes/
    GET    /notes/{note_id}
    PUT    /notes/{note_id}
    DELETE /notes/{note_id}

All operations use the authenticated user to enforce ownership.

This means the API does not trust a user-provided `user_id`.

---

# 12. Pydantic Schemas

Authentication introduced dedicated schemas.

## UserCreate

Used during registration.

Fields:

- `email`
- `password`

The password has a minimum length requirement.

## UserLogin

Used during login.

Fields:

- `email`
- `password`

## Token

Represents the authentication response.

Fields:

- `access_token`
- `token_type`

## UserResponse

Represents the public user information.

Fields:

- `id`
- `email`

The password and password hash are intentionally excluded.

---

# 13. HTTP Status Codes

The authentication endpoints use meaningful HTTP status codes.

## Registration

Successful registration:

    201 Created

Duplicate email:

    400 Bad Request

## Login

Successful login:

    200 OK

Invalid credentials:

    401 Unauthorized

## Protected resources

Unauthenticated or invalid authentication:

    401 Unauthorized

Resource does not belong to the authenticated user:

    404 Not Found

Returning `404 Not Found` for a note belonging to another user also prevents the API from unnecessarily revealing that the resource exists.

---

# 14. Authentication vs Authorization

A key concept from this phase:

### Authentication

Answers:

    "Who are you?"

Implemented using:

- email/password
- password hashing
- JWT
- `get_current_user`

### Authorization

Answers:

    "Are you allowed to access this?"

Implemented using:

- `current_user.id`
- `Note.user_id`
- ownership filters in SQLAlchemy queries

Example:

    User A
      ↓
    JWT → user_id = 1
      ↓
    GET /notes/42
      ↓
    Query:
    note.id = 42
    AND
    note.user_id = 1

If note 42 belongs to User B, User A cannot access it.

---

# 15. Testing Authentication and Authorization

Authentication and ownership behavior were covered by integration tests.

The test suite verifies:

- user registration
- user login
- JWT authentication
- protected endpoints
- note creation
- note retrieval
- note listing
- validation errors
- user-specific note isolation

The final test suite contains:

    13 passed

This confirms that the authentication and authorization layer works together with the existing notes functionality.

---

# 16. Important Lessons

## Never trust user IDs from clients

Bad approach:

    POST /notes/

    {
        "title": "...",
        "content": "...",
        "user_id": 123
    }

The client should not control ownership.

Instead:

    current_user.id

is derived from the authenticated JWT.

---

## Passwords should never be stored directly

Never store:

    password = "password123"

Store a secure password hash instead.

---

## Authentication should be centralized

Rather than repeating JWT validation in every endpoint, FastAPI dependencies provide a reusable authentication layer.

---

## Authorization belongs close to the database query

Instead of retrieving a note and checking ownership afterward, ownership can be included directly in the query:

    select(Note).where(
        Note.id == note_id,
        Note.user_id == current_user.id,
    )

This reduces the risk of accidentally exposing another user's resource.

---

# 17. Phase 03 Final State

At the end of Phase 03, NoteKeeper has:

- User registration
- Secure password hashing
- User login
- JWT access tokens
- Current-user dependency
- Protected API endpoints
- User-scoped notes
- Ownership-based authorization
- Authentication schemas
- Authorization tests
- 13 passing tests

The application has now moved from a single-user CRUD API toward a real multi-user backend.

---
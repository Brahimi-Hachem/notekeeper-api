&#x20;

# **PHASE 0: Backend Foundations \& Project Architecture**







&#x09;	    ┌─────────────────┐

&#x20;                   │   Web / Mobile  │

&#x20;                   │      Client     │

&#x20;                   └────────┬────────┘

&#x20;                            │

&#x20;                            │ HTTP/HTTPS

&#x20;                            ▼

&#x20;                   ┌─────────────────┐

&#x20;                   │    FastAPI      │

&#x20;                   │      API        │

&#x20;                   └────────┬────────┘

&#x20;                            │

&#x20;             ┌──────────────┼──────────────┐

&#x20;             │              │              │

&#x20;             ▼              ▼              ▼

&#x20;        Authentication   Services     API validation

&#x20;             │              │

&#x20;             │              ▼

&#x20;             │        Repositories

&#x20;             │              │

&#x20;             │              ▼

&#x20;             │        SQLAlchemy

&#x20;             │              │

&#x20;             └──────────────┼──────────────┘

&#x20;                            ▼

&#x20;                      PostgreSQL





**our program will**



1. Receive HTTP request

2\. Validate the request

3\. Identify the user

4\. Check authorization

5\. Query PostgreSQL

6\. Transform database records

7\. Return JSON





**HTTP fundamentals**



Method	Meaning			Example

GET	Retrieve		GET /notes

POST	Create			POST /notes

PUT	Replace			PUT /notes/42

PATCH	Partially update	PATCH /notes/42

DELETE	Delete			DELETE /notes/42









**Status codes:**



200 OK

201 Created

204 No Content



400 Bad Request

401 Unauthorized    I DON'T KNOW WHO U R

403 Forbidden	    U R NOT AUTHORIZZED 

404 Not Found

409 Conflict

422 Validation Error



500 Internal Server Error









The database is 



user / note / tag





users

&#x20; │

&#x20; └──────< notes >──────< note\_tags >──────< tags



User 1 ──────────── N Notes

Notes N ─────────── N Tags





User			

├── id

├── email

├── password\_hash

└── created\_at





Note

├── id

├── user\_id

├── title

├── content

├── created\_at

└── updated\_at







Tag

├── id

└── name









**SQLAlchemy**





SQLAlchemy is an ORM, among other things.

ORM:

Object-Relational Mapper



It allows database tables to be represented as Python objects/classes.





Python

&#x20;  │

&#x20;  ▼

SQLAlchemy

&#x20;  │

&#x20;  ▼

SQL

&#x20;  │

&#x20;  ▼

PostgreSQL









SQLAlchemy

= application/database model



Alembic

= database schema evolution









1\. API

A contract through which another application communicates with your backend.



2\. REST

A style of designing APIs around resources and HTTP semantics.



3\. FastAPI

The framework we'll use to expose our Python application over HTTP.



4\. Pydantic

Validates and structures data entering/leaving the API.



5\. PostgreSQL

Our relational database and source of truth.



6\. SQLAlchemy

Our Python/database interaction layer.



7\. Alembic

Tracks and applies database schema changes.



8\. JWT

A mechanism we'll use to carry authenticated user information between requests.



9\. Service/Repository architecture

Separates HTTP concerns, business logic, and data access.



10\. CI/CD

Automatically validates and eventually deploys our application when code changes.


































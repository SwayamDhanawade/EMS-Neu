# Employee Management System API

This is a Python backend for an Employee Management System built with FastAPI and SQLAlchemy ORM.

The system exposes a RESTful CRUD API for employees (create, read, update, delete) with automatic schema creation, email uniqueness enforcement, and meaningful error handling.

The backend is backed by unit tests for each layer (repository, service, and API), using in‑memory SQLite for repository tests and mocked dependencies for higher‑level layers, making it easy to run locally and evaluate.

---

## Features

- Full CRUD for employees (create, read, update, delete)
- Three-layer architecture with clear responsibility separation
- SQLAlchemy ORM with PostgreSQL/MySQL support
- SQLite default for zero-config local development
- Environment-based configuration via `pydantic-settings`
- Schema validation with Pydantic v2 (`EmailStr`, required/optional fields)
- Custom service-layer exceptions mapped to proper HTTP responses (`404`, `409`)
- Automatic table creation on startup
- Swagger/OpenAPI docs at `/docs`
- Comprehensive test suite covering all layers

---

## Tech Stack

| Technology | Purpose |
|---|---|
| Python 3.13 | Runtime |
| FastAPI | Web framework |
| SQLAlchemy 2.0 | ORM and database access |
| Pydantic v2 + pydantic-settings | Schema validation and configuration |
| PostgreSQL | Production databases (via `DATABASE_URL`) |
| SQLite | Local development default |
| pytest + httpx | Testing (TestClient) |

---

## Project Structure

```
app/
├── api/                # Router layer — HTTP endpoints, DI wiring
├── services/           # Service layer — business rules, validation
├── repositories/       # Repository layer — database queries
├── models/             # SQLAlchemy ORM models
├── schemas/            # Pydantic request/response schemas
├── core/               # Config, engine, session, custom exceptions
└── main.py             # FastAPI app entry point
tests/
├── conftest.py         # Shared fixtures
├── test_repository.py  # Repository tests (real in-memory DB)
├── test_service.py     # Service tests (mocked repository)
└── test_api.py         # API tests (dependency overrides)
```

---

## Setup

### 1. Clone and create a virtual environment

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# macOS / Linux
source venv/bin/activate
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure database (optional)

The app defaults to a local SQLite database. To use PostgreSQL or MySQL, set the
`DATABASE_URL` environment variable:

```bash
# SQLite (default — nothing to do)

# PostgreSQL
export DATABASE_URL="postgresql://user:password@localhost:5432/ems"

# MySQL
export DATABASE_URL="mysql+pymysql://user:password@localhost:3306/ems"
```

### 4. Run the server

```bash
uvicorn app.main:app --reload
```

Open [http://localhost:8000/docs](http://localhost:8000/docs) for the interactive Swagger UI.

---

## Environment Variables

| Variable | Default | Description |
|---|---|---|
| `DATABASE_URL` | `sqlite:///./employees.db` | SQLAlchemy database connection string |

Copy `.env.example` to `.env` and edit as needed. The app reads `.env` automatically
via `pydantic-settings`.

---

## API Endpoints

| Method | Path | Description | Success | Errors |
|---|---|---|---|---|
| `POST` | `/employees` | Create a new employee | `201` | `409` duplicate email |
| `GET` | `/employees` | List all employees | `200` | — |
| `GET` | `/employees/{id}` | Get employee by ID | `200` | `404` not found |
| `PUT` | `/employees/{id}` | Update employee fields | `200` | `404` not found, `409` duplicate email |
| `DELETE` | `/employees/{id}` | Delete an employee | `204` | `404` not found |
| `GET` | `/health` | Health check | `200` | — |

---

## Example Requests and Responses

### Create employee

```bash
curl -X POST http://localhost:8000/employees \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Alice Johnson",
    "email": "alice@example.com",
    "department": "Engineering",
    "date_joined": "2024-01-15"
  }'
```

**Success (201):**

```json
{
  "id": 1,
  "name": "Alice Johnson",
  "email": "alice@example.com",
  "department": "Engineering",
  "date_joined": "2024-01-15"
}
```

**Duplicate email (409):**

```json
{
  "detail": "Employee with email alice@example.com already exists"
}
```

### Update employee (partial)

```bash
curl -X PUT http://localhost:8000/employees/1 \
  -H "Content-Type: application/json" \
  -d '{"department": "Product"}'
```

**Success (200):**

```json
{
  "id": 1,
  "name": "Alice Johnson",
  "email": "alice@example.com",
  "department": "Product",
  "date_joined": "2024-01-15"
}
```

---

## Architecture Notes

| Layer | File | Responsibility |
|---|---|---|
| **Router** | `app/api/` | HTTP handling, dependency injection, response serialization |
| **Service** | `app/services/` | Business rules, validation, raising domain exceptions |
| **Repository** | `app/repositories/` | Direct database access via SQLAlchemy |

The service layer never imports FastAPI directly — it raises plain Python
exceptions (`EmployeeNotFoundError`, `DuplicateEmailError`) that the router
layer maps to HTTP responses via global exception handlers.

---

## Running Tests

```bash
pytest
```

The suite includes **35 tests** across three layers:

| Test file | Approach | What it verifies |
|---|---|---|
| `tests/test_repository.py` | Real in-memory SQLite database | Persistence, queries, ordering |
| `tests/test_service.py` | Mocked `EmployeeRepository` via `MagicMock` | Business rules, exception paths, repository interaction |
| `tests/test_api.py` | FastAPI `TestClient` with dependency overrides | HTTP status codes, response bodies, error mapping |

---
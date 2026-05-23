# Employee Management System

## Tech Stack

- FastAPI (Python 3)
- SQLAlchemy ORM
- PostgreSQL / MySQL (SQLite default for local development)
- Layered architecture: router → service → repository

## Development Setup

1. Create a virtual environment and install dependencies:

   ```bash
   python -m venv venv
   source venv/bin/activate   # or venv\Scripts\activate on Windows
   pip install -r requirements.txt
   ```

2. Set `DATABASE_URL` (optional — defaults to local SQLite):

   ```bash
   # SQLite (default, no action needed)
   # PostgreSQL
   export DATABASE_URL="postgresql://user:password@localhost:5432/ems"
   # MySQL
   export DATABASE_URL="mysql+pymysql://user:password@localhost:3306/ems"
   ```

3. Run the development server:

   ```bash
   uvicorn app.main:app --reload
   ```

   The API will be available at `http://localhost:8000`.

## API Endpoints

| Method | Path             | Description              |
|--------|------------------|--------------------------|
| GET    | `/health`        | Health check             |
| GET    | `/employees/ping`| Router connectivity test |

## Phase 1

This phase sets up the project skeleton, configuration, and database wiring only.
Business logic, models, schemas, CRUD endpoints, validation, error handling, and
tests will be added in later phases.

# About

Small FastAPI service for querying service-availability data from a SQLite database with filtering and pagination. Built with FastAPI, SQLAlchemy, and Pydantic; tested with pytest against an in-memory SQLite DB, and containerized via Docker with separate build stages for running the API and running tests.

# Running the API

To run the API:

```
docker compose up backend
```

The API will be available at `https://localhost:8000` (interactive docs at `/docs`).

To run the tests:

```
docker compose run --rm test
```
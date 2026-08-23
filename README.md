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

# Example usage

```
$ curl -s "http://localhost:8000/list?dmin=2020-01-01&service=pdf_generator&service=report_exporter&limit=4&offset=80" | jq
{
  "total": 850,
  "limit": 4,
  "offset": 80,
  "results": [
    {
      "date": "2020-02-10",
      "service": "pdf_generator",
      "availability": 97.11
    },
    {
      "date": "2020-02-10",
      "service": "report_exporter",
      "availability": 99.6
    },
    {
      "date": "2020-02-11",
      "service": "pdf_generator",
      "availability": 96.13
    },
    {
      "date": "2020-02-11",
      "service": "report_exporter",
      "availability": 97.89
    }
  ]
}

```
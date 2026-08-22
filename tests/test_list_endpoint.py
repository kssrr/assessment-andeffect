from datetime import date
from app import models


def seed(db, rows):
    db.add_all([models.Availability(**r) for r in rows])
    db.commit()


def test_list_no_filters_returns_seeded_rows(client, db_session):
    seed(db_session, [
        {"date": date(2026, 1, 1), "service": "exporter", "availability": 0.95},
        {"date": date(2026, 1, 2), "service": "importer", "availability": 0.97},
    ])

    response = client.get("/list")

    assert response.status_code == 200
    body = response.json()
    assert body["total"] == 2
    assert body["limit"] == 100
    assert body["offset"] == 0
    assert len(body["results"]) == 2
    assert body["results"][0] == {
        "date": "2026-01-01",
        "service": "yoga",
        "availability": 3.0,
    }


def test_list_total_reflects_filtered_count_not_page_size(client, db_session):
    seed(db_session, [
        {"date": date(2026, 1, i), "service": "yoga", "availability": 1.0}
        for i in range(1, 6)
    ] + [
        {"date": date(2026, 1, 1), "service": "pilates", "availability": 1.0},
    ])

    response = client.get("/list", params={"service": "yoga", "limit": 2})

    body = response.json()
    assert body["total"] == 5 
    assert len(body["results"]) == 2
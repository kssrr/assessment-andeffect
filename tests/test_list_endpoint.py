import pytest
from datetime import date

from app import models

@pytest.fixture
def seeded(db_session):
    rows = [
        models.Availability(date=date(2024, 1, 1), service="a", availability=0.1),
        models.Availability(date=date(2024, 1, 2), service="a", availability=0.2),
        models.Availability(date=date(2024, 1, 1), service="b", availability=0.3),
        models.Availability(date=date(2024, 1, 2), service="b", availability=0.4),
        models.Availability(date=date(2024, 1, 1), service="c", availability=0.5),
        models.Availability(date=date(2024, 1, 2), service="c", availability=0.6)
    ]
    db_session.add_all(rows)
    db_session.commit()
    return rows

def test_pagination(client, seeded):
    # testen ob total, filtered count & 
    # results mit pagination übereinstimmen
    params = [("service", "a"), ("service", "b"), ("limit", 1)]
    # ^ sollte vier zeilen matchen

    # Erster call -> erwartetes `total`:
    first_page = client.get("/list", params=params + [("offset", 0)]).json()
    total = first_page["total"]
    assert total == 4, f"`total` is wrong. Expected: 4, got: {total}."

    # alle pages mit einzelnen results durchgehen
    # und schauen ob alles stabil bleibt
    seen_keys = set()
    for offset in range(total):
        resp = client.get("/list", params=params + [("offset", offset)])
        assert resp.status_code == 200, "Got unexpected (non-200) response from client."
        body = resp.json()

        # einzelne pages sollten richtiges `total` reporten
        assert body["total"] == total, "`total` reported on individual pages does not match true `total`."
        assert len(body["results"]) == 1, "Wrong page size (`limit` not respected)."

        row = body["results"][0]
        #assert row["service"] in ("a", "b") 
        seen_keys.add((row["date"], row["service"]))

    assert len(seen_keys) == total, "Number of counted individual responses does not match `total`."

    # wenn wir nach der letzten page weitergehen sollten zwar keine
    # results mehr kommen, aber `total` sollte weiterhin stimmen:
    resp = client.get("/list", params=params + [("offset", total)])
    body = resp.json()
    assert body["total"] == total, "Wrong `total` reported when paging past end."
    assert body["results"] == [], f"Expected no results when paging past the end, got {body['results']}."
from datetime import date
from fastapi import FastAPI, Depends, Query
from sqlalchemy.orm import Session

from app.database import get_db
from app import models, schemas

app = FastAPI()

@app.get("/")
def root():
    return {"status": "ok"}

@app.get("/list", response_model=schemas.AvailabilityPage)
def list_items(
    dmin: date | None = Query(None, description="From (YYYY-MM-DD)"),
    dmax: date | None = Query(None, description="From (YYYY-MM-DD)"),
    service: list[str] | None = Query(None, description="Service(s)"),
    limit: int = Query(100, ge=1, le=1000, description="Max results to return"),
    offset: int = Query(0, ge=0, description="Number of results to skip"),
    db: Session = Depends(get_db)
):
    query = db.query(models.Availability)

    if dmin is not None:
        query = query.filter(models.Availability.date >= dmin)
    if dmax is not None:
        query = query.filter(models.Availability.date <= dmax)
    if service is not None:
        query = query.filter(models.Availability.service.in_(service))

    total = query.count()
    result = query.order_by(models.Availability.date).offset(offset).limit(limit).all()

    return {"total": total, "limit": limit, "offset": offset, "results": result}
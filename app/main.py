from datetime import date
from fastapi import FastAPI, Depends, Query
from sqlalchemy.orm import Session

from app.database import SessionLocal
from app import models, schemas

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def root():
    return {"status": "ok"}

@app.get("/list", response_model=list[schemas.AvailabilityResponse])
def list_items(
    dmin: date | None = Query(None, description="From (YYYY-MM-DD)"),
    dmax: date | None = Query(None, description="From (YYYY-MM-DD)"),
    service: str | None = Query(None, description="Service"),
    db: Session = Depends(get_db)
):
    query = db.query(models.Availability)

    if dmin is not None:
        query = query.filter(models.Availability.date >= dmin)
    if dmax is not None:
        query = query.filter(models.Availability.date <= dmax)
    if service is not None:
        query = query.filter(models.Availability.service == service)

    result = query.all()

    return result
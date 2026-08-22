from contextlib import asynccontextmanager
from datetime import date
from fastapi import FastAPI, Depends, Query, Request
from sqlalchemy import func
from sqlalchemy.orm import Session

from app.database import SessionLocal
from app import models, schemas


@asynccontextmanager
async def lifespan(app: FastAPI):
    db = SessionLocal()
    try:
        # wenn der user keine date range angibt
        # wollen wir einfach alle daten (ganze range)
        # ausgeben. Min & max date vorab im Kontext 
        # speichern, um nicht jedes mal wenn der Endpoint
        # aufgerufen wird min & max queries machen zu
        # müssen:
        dmin, dmax = db.query(
            func.min(models.Availability.date),
            func.max(models.Availability.date),
        ).one()
        app.state.date_bounds = (dmin, dmax)
    finally:
        db.close()
    yield 

app = FastAPI(lifespan=lifespan)

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
    request: Request,
    dmin: date | None = Query(None, description="From (YYYY-MM-DD)"),
    dmax: date | None = Query(None, description="From (YYYY-MM-DD)"),
    db: Session = Depends(get_db)
):
    # falls keine date range angegeben, ganze date
    # range benutzen:
    default_min, default_max = request.app.state.date_bounds
    dmin = dmin or default_min
    dmax = dmax or default_max

    result = (
        db
        .query(models.Availability)
        .filter(models.Availability.date.between(dmin, dmax))
        .all()
    )

    return result
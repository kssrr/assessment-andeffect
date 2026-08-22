from datetime import date
from pydantic import BaseModel

class AvailabilityOut(BaseModel):
    date: date
    service: str
    availability: float

    model_config = {"from_attributes": True}
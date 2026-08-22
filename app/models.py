from sqlalchemy import Column, Date, String, Float
from app.database import Base

class Availability(Base):
    __tablename__ = "service_availabilities"
    date = Column(Date, primary_key=True, index=True)
    service = Column(String, primary_key=True, index=True)
    availability = Column(Float)
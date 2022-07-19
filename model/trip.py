from datetime import date, datetime, time
from typing import Optional
from pydantic import BaseModel
from .model import ApiResponse

class Trip(BaseModel):
    id: int
    bus_name: str
    loc_name: str
    price: float
    seat: int
    departure_date: date
    departure_time: time
    status: int

class TripsResponse(ApiResponse):
    data: list[Trip]

class TripResponse(ApiResponse):
    data: Trip

class AddTripRequest(BaseModel):
    loc_id: int
    bus_id: int
    departure_date: date
    departure_time: time

class UpdateTripRequest(BaseModel):
    trip_id: int
    departure_date: date
    departure_time: time

class EndTripRequest(BaseModel):
    trip_id: int

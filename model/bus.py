from datetime import datetime
from typing import Optional
from pydantic import BaseModel
from .model import ApiResponse

class AddBusRequest(BaseModel):
    name: str
    price: float
    type_id: int
    loc_id: int
    created_date: datetime

class UpdateBusRequest(BaseModel):
    bus_id: int
    price: float
    status: int

class BusWithType(BaseModel):
    id: int
    bus_name: str
    type_name: str
    bus_desc: Optional[str]
    num_of_seat: int
    price: float
    status: int

class BusesResponse(ApiResponse):
    data: list[BusWithType]

class Bus(BaseModel):
    id: int
    bus_name: str
    bus_desc: Optional[str]
    num_of_seat: int
    price: float
    status: int

class BusResponse(ApiResponse):
    data: Bus

class BusName(BaseModel):
    bus_name: str

class BusLocationResponse(ApiResponse):
    data: list[BusName]
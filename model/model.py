from datetime import date, datetime, time
from typing import Optional
from pydantic import BaseModel

class ApiResponse(BaseModel):
    data: Optional[object]
    is_success: bool
    message: str

class BusSeat(BaseModel):
    id: int
    bus_id: int
    seat_name: str
    seat_desc: Optional[str]
    status: int

class BusSeatsResponse(ApiResponse):
    data: list[BusSeat]

class BookingDetail(BaseModel):
    id: int
    booking_id: int
    trip_id: int
    description: Optional[str]
    seat_id: int
    price: float

class BookingDetailResponse(ApiResponse):
    data: BookingDetail

class BookingDetailTrip(BaseModel):
    trip_id: int

class BookingDetailTripResponse(ApiResponse):
    data: BookingDetailTrip

class UpdateTransactionRequest(BaseModel):
    booking_id: int
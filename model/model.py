from datetime import date, datetime, time
from optparse import Option
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

class BusSeatIdResponse(ApiResponse):
    data: Optional[int]

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

class AddBookingDetailRequest(BaseModel):
    booking_id: int
    trip_id: int
    seat_id: int
    price: float

class UpdateBusSeat(BaseModel):
    seat_id: int
    status: int

class AddOnlinePaymentRequest(BaseModel):
    booking_id: int
    pay_date: date
    cus_id: int

class AddOfflinePaymentRequest(BaseModel):
    booking_id: int
    booking_date: date
    cus_id: int
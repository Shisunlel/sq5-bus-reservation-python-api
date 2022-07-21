from datetime import date, datetime, time
from typing import Optional
from pydantic import BaseModel
from .model import ApiResponse

class Booking(BaseModel):
    id: int
    user_id: int
    description: Optional[str]
    payment: float
    booking_date: date
    status: int

class BookingsResponse(ApiResponse):
    data: list[Booking]

class BookingResponse(ApiResponse):
    data: Booking

class UserBooking(BaseModel):
    user_id: Optional[int]
    user_name: Optional[str]

class UsersBookingResponse(ApiResponse):
    data: list[UserBooking]

class UserBookingResponse(ApiResponse):
    data: UserBooking

class AddBookingRequest(BaseModel):
    user_id: int
    payment: float
    booking_date: date

class AddBookingResponse(ApiResponse):
    data: int

class UpdateBookingStatus(BaseModel):
    status: int
    booking_id: int
from datetime import date, datetime, time
from turtle import st
from typing import Optional
from pydantic import BaseModel
from .model import ApiResponse

class Booking(BaseModel):
    booking_id: str
    trip_id: str
    destination: str
    booking_date: str
    price: str
    bus_name: str
    seat: str
    paid_status: str

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
from datetime import date, datetime, time
from optparse import Option
from typing import Optional
from pydantic import BaseModel

class RegisterModel(BaseModel):
    user_name: str
    user_pass: str
    email: str


class ApiResponse(BaseModel):
    data: Optional[object]
    is_success: bool
    message: str

class UserModel(BaseModel):
    user_id: Optional[int]
    user_name: str
    user_pass: str
    first_name: Optional[str]
    last_name: Optional[str]
    date_of_birth: Optional[date]
    user_desc: str
    phone: Optional[str]
    email: str
    created_date: Optional[date]
    status: Optional[int]
class UsersResponse(ApiResponse):
    data: list[UserModel]

class UserModelForDashboard(BaseModel):
    user_id: Optional[int]
    user_name: Optional[str]
    user_pass: Optional[str]
    first_name: Optional[str]
    last_name: Optional[str]
    date_of_birth: Optional[date]
    email: Optional[str]
    phone: Optional[str]
    user_desc: Optional[str]
    status: Optional[int]
class UsersResponseForDashboard(ApiResponse):
    data: list[UserModelForDashboard]

class UserResponse(ApiResponse):
    data: Optional[UserModel]

class LocationModel(BaseModel):
    loc_id: int
    loc_name: str

class LocationsResponse(ApiResponse):
    data: list[LocationModel]

class LocationResponse(ApiResponse):
    data: LocationModel
class UpdateInfoRequest(BaseModel):
    user_name: str
    first_name: str
    last_name: str
    phone: str
    email: str
    date_of_birth: str

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
class UpdatePasswordRequest(BaseModel):
    user_pass: str
    user_name: str
class UpdateUserRequest(BaseModel):
    user_name: str
    user_pass: str
    phone: str
    email: str
    user_role: str

class DeleteUserRequest(BaseModel):
    user_name: str

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

class UpdateTransactionRequest(BaseModel):
    booking_id: int
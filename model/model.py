from datetime import date
from lib2to3.pytree import Base
from re import I
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

class UsersModelData(BaseModel):
    users: list[UserModel]

class UsersResponse(ApiResponse):
    data: UsersModelData

class UserModelForDashboard(BaseModel):
    user_id: Optional[int]
    user_name: str
    user_pass: str
    first_name: Optional[str]
    last_name: Optional[str]
    date_of_birth: Optional[date]
    email: str
    phone: Optional[str]
    user_desc: str
    status: Optional[int]
class UsersModelDataForDashboard(BaseModel):
    users: list[UserModelForDashboard]
class UsersResponseForDashboard(ApiResponse):
    data: UserModelForDashboard

class UserModelData(BaseModel):
    user: UserModel

class UserResponse(ApiResponse):
    data: UserModelData

class LocationModel(BaseModel):
    loc_name: str

class LocationModelData(BaseModel):
    locations: list[LocationModel]

class LocationResponse(ApiResponse):
    data: LocationModelData
    
class UpdateInfoRequest(BaseModel):
    first_name: str
    last_name: str
    phone: str
    email: str
    date_of_birth: str

class AddBusRequest(BaseModel):
    name: str
    price: float
    type_id: int
    created_date: date

class UpdateBusRequest(BaseModel):
    bus_id: int
    price: float
    status: int

from datetime import date
from typing import Optional
from pydantic import BaseModel
from .model import ApiResponse

class RegisterModel(BaseModel):
    user_name: str
    user_pass: str
    email: str

class UserModel(BaseModel):
    user_id: Optional[int]
    user_name: str
    user_pass: str
    first_name: Optional[str]
    last_name: Optional[str]
    date_of_birth: Optional[date]
    user_desc: Optional[str]
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

class UpdateInfoRequest(BaseModel):
    user_name: str
    first_name: str
    last_name: str
    phone: str
    email: str
    date_of_birth: str

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


from lib2to3.pytree import Base
from pydantic import BaseModel

class RegisterModel(BaseModel):
    user_name: str
    user_pass: str
    email: str


class ApiResponse(BaseModel):
    data: None
    is_success: bool
    message: str

class UserModel(BaseModel):
    user_id: int
    user_name: str
    user_pass: str
    first_name: str
    last_name: str
    date_of_birth: str | None
    user_desc: str
    phone: str | None
    email: str
    created_date: str
    status: int

class UsersModelData(BaseModel):
    users: list[UserModel]

class UsersResponse(ApiResponse):
    data: UsersModelData

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
from pydantic import BaseModel
from .model import ApiResponse

class LocationModel(BaseModel):
    loc_id: int
    loc_name: str

class LocationsResponse(ApiResponse):
    data: list[LocationModel]

class LocationResponse(ApiResponse):
    data: LocationModel
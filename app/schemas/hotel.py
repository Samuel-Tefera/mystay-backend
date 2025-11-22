from pydantic import BaseModel
from typing import Optional

from app.schemas.room import RoomDisaply

class Location(BaseModel):
  latitude: float
  longitude: float

class HotelBase(BaseModel):
  name: str
  description: Optional[str] = None
  address: str
  rating: float
  exact_location: Location
  contact_number: str
  email: str

class HotelCreate(HotelBase):
  manager_id : int

class HotelUpdate(BaseModel):
  name: Optional[str] = None
  description: Optional[str] = None
  address: Optional[str] = None
  rating: Optional[float] = None
  exact_location: Optional[Location] = None
  contact_number: Optional[str] = None
  email: Optional[str] = None

class HotelDisplay(HotelBase):
  id: int
  manager_id: int
  rooms: Optional[list[RoomDisaply]] = []

  class config:
    orm_mode: True

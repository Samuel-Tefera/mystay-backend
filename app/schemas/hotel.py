from pydantic import BaseModel, EmailStr
from typing import Optional

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
  city: Optional[str] = None
  country: Optional[str] = None
  latitude: Optional[float] = None
  longitude: Optional[float] = None
  contact_number: Optional[str] = None
  email: Optional[str] = None

class HotelDisplay(HotelBase):
  id: int
  manager_id: int
  # rooms: list[Room] : []

  class config:
    orm_mode: True

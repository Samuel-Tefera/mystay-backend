from datetime import datetime
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


class HotelUpdate(BaseModel):
  name: Optional[str] = None
  description: Optional[str] = None
  address: Optional[str] = None
  rating: Optional[float] = None
  exact_location: Optional[Location] = None


class HotelDisplay(HotelBase):
  id: int
  manager_id: int

  class Config:
    orm_mode: True


class HotelDisplayDetail(HotelDisplay):
  rooms: list[RoomDisaply] = None


class HotelApplicationBase(BaseModel):
  # Manager Info
  manager_name : str
  manager_email : str

  # Hotel Info
  hotel_name : str
  hotel_address : str


class HotelApplicationCreate(HotelApplicationBase):
  manager_phone : Optional[str] = None
  hotel_description : Optional[str] = None
  hotel_star_rating : Optional[int] = None
  hotel_exact_location : Location


class HotelApplicationDisplay(HotelApplicationBase):
  id: int
  status : str
  created_at: datetime

  class Config:
    orm_mode: True


class HotelApplicationDetailDisplay(HotelApplicationDisplay):
  manager_phone : Optional[str] = None
  hotel_description : Optional[str] = None
  hotel_star_rating : Optional[int] = None
  hotel_exact_location : Location

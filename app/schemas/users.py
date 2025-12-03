from datetime import datetime
from typing import Optional
from pydantic import BaseModel

from app.schemas.hotel import HotelDisplay


# Input Schema Hotel Manager
class HotelManagerCreate(BaseModel):
  name: str
  email: str
  phone: str | None = None


# Output Schema Hotel Manager
class HotelManagerDisplay(BaseModel):
  id: int
  name: str
  email: str
  phone: str | None = None
  is_approved: bool
  hotel: Optional[HotelDisplay] = None

  class Config:
    orm_mode = True

# Guest Output
class GuestDisplay(BaseModel):
  id: int
  email: str
  full_name: str
  avater_url: str
  created_at: datetime

  model_config = {
    'from_attributes': True
  }

  # class Config:
  #   orm_mode = True


class AdminLogin(BaseModel):
  email: str
  password: str

from typing import Optional
from pydantic import BaseModel

from app.models.room import BedType, RoomType

class RoomBase(BaseModel):
  room_number: str
  room_type: RoomType
  price_per_night: float
  description: str
  bed_type: BedType


class RoomUpdate(BaseModel):
  room_number: Optional[str] = None
  room_type: Optional[RoomType]  = None
  price_per_night: Optional[float] = None
  description: Optional[str] = None
  bed_type: Optional[BedType] = None


class HotelView(BaseModel):
  id: int
  name: str
  rating: int
  address: str


class RoomDisaply(RoomBase):
  id: int
  hotel_id: int
  image_url: str

  hotel: HotelView

  class config:
    orm_mode = True

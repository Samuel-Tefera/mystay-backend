from typing import Optional
from pydantic import BaseModel

from app.models.room import BedType, RoomType

class RoomBase(BaseModel):
  room_number: str
  room_type: RoomType
  price_per_night: float
  description: str
  bed_type: BedType
  image_url: str


class RoomUpdate(BaseModel):
  room_number: Optional[str] = None
  room_type: Optional[RoomType]  = None
  price_per_night: Optional[float] = None
  description: Optional[str] = None
  bed_type: Optional[BedType] = None
  image_url: Optional[str] = None


class RoomDisaply(RoomBase):
  id: int
  hotel_id: int

  class config:
    orm_mode = True

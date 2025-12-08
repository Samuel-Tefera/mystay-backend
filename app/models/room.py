from sqlalchemy import Boolean, Column, Float, ForeignKey, Integer, String, Enum as SQLEnum
from sqlalchemy.orm import relationship

from enum import Enum

from app.database import Base


class RoomType(str, Enum):
  SINGLE = 'single'
  DOUBLE = 'double'
  SUITE = 'suite'
  DELUXE = 'deluxe'
  STANDARD = 'standard'

class BedType(str, Enum):
  QUEEN = 'queen'
  KING = 'king'
  TWIN = 'twin'


class Room(Base):
  __tablename__ = 'rooms'

  id = Column(Integer, primary_key=True, index=True)
  room_number = Column(String, nullable=False)
  room_type = Column(SQLEnum(RoomType), nullable=False, default=RoomType.SINGLE)
  price_per_night = Column(Float, nullable=False)
  description = Column(String, nullable=True)
  bed_type = Column(SQLEnum(BedType), nullable=False, default=BedType.KING)
  image_url = Column(String, nullable=False)

  hotel_id = Column(Integer, ForeignKey('hotels.id', ondelete='CASCADE'), nullable=False)
  hotel = relationship('Hotel', back_populates='rooms')

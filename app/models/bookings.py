from sqlalchemy import Column, Date, DateTime, Float, ForeignKey, Integer, Enum as SQLEnum
from sqlalchemy.orm import relationship

from datetime import datetime
from enum import Enum

from app.database import Base


class BookingStatus(str, Enum):
  PENDING = 'pending'
  CONFIRMED = 'confirmed'
  CANCELLED = 'cancelled'
  COMPLETED = 'completed'


class Booking(Base):
  __tablename__ = 'bookings'

  id = Column(Integer, primary_key=True, index=True)

  guest_id = Column(Integer, ForeignKey('guests.id'), nullable=False)
  room_id = Column(Integer, ForeignKey('rooms.id'), nullable=False)
  hotel_id = Column(Integer ,ForeignKey('hotels.id'), nullable=False)

  check_in = Column(Date, nullable=False)
  check_out = Column(Date, nullable=False)
  nights = Column(Integer, nullable=False)

  price_per_night = Column(Float, nullable=False)
  total_price = Column(Float, nullable=False)

  status = Column(SQLEnum(BookingStatus), default=BookingStatus.PENDING)

  created_at = Column(DateTime, default=datetime.utcnow)
  updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

  guest = relationship("Guest", back_populates="bookings")
  room = relationship("Room", back_populates="bookings")

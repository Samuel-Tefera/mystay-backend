from datetime import date
from pydantic import BaseModel

from app.models.bookings import BookingStatus
from app.models.payments import PaymentMethod


class BookingBase(BaseModel):
  check_in: date
  check_out: date


class BookingCreate(BookingBase):
  room_id: int
  payment_method: PaymentMethod


class BookingDisplay(BookingBase):
  id: int
  room_id: int
  status: BookingStatus
  total_price: float

  class Config:
    orm_mode: True

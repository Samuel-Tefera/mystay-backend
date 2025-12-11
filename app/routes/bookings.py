from fastapi import APIRouter, Depends, HTTPException

from sqlalchemy.orm import Session
from app.core.dependencies import require_admin, require_guest, require_hotel_manager

from app.database import get_db
from app.models.bookings import Booking
from app.models.payments import Payment, PaymentMethod
from app.models.room import Room
from app.models.users import Guest
from app.schemas.bookings import BookingCreate, BookingDisplay
from app.utils.booking_services import is_room_available


router = APIRouter(prefix='/bookings', tags=['Bookings'])

# Reserve Room
@router.post('/', response_model=BookingDisplay)
def create_booking(
  new_booking: BookingCreate,
  guest_data = Depends(require_guest),
  db: Session = Depends(get_db)):

  guest = db.query(Guest).filter(Guest.id == int(guest_data['sub'])).first()

  if not guest:
    raise HTTPException(status_code=400, detail='Bad request')

  room = db.query(Room).filter(Room.id == new_booking.room_id).first()
  if not room:
    raise HTTPException(status_code=404, detail='No room found to make booking')

  available = is_room_available(db, new_booking.room_id, new_booking.check_in, new_booking.check_out)

  if not available:
    raise HTTPException(status_code=409, detail='Room is not available for the selected dates')

  num_of_nights = (new_booking.check_out - new_booking.check_in).days
  total_price = room.price_per_night * num_of_nights

  db_booking = Booking(
    guest_id = guest.id,
    room_id = new_booking.room_id,
    hotel_id = room.hotel_id,
    check_in = new_booking.check_in,
    check_out = new_booking.check_out,
    nights = num_of_nights,
    price_per_night = room.price_per_night,
    total_price = total_price
  )

  db.add(db_booking)
  db.commit()
  db.refresh(db_booking)

  payment_status = 'unpaid'

  if new_booking.payment_method == PaymentMethod.MOBILE or new_booking.payment_method == PaymentMethod.CARD:
    payment_status = 'paid'

  db_payment = Payment(
    booking_id = db_booking.id,
    guest_id = guest.id,
    amount = total_price,
    method = new_booking.payment_method,
    status = payment_status,
  )

  db.add(db_payment)
  db.commit()
  db.refresh(db_payment)

  return db_booking

# Guest view my bookings
@router.get('/', response_model=list[BookingDisplay])
def view_bookings(
  guest_data = Depends(require_guest),
  db: Session = Depends(get_db)):
  # filter by status (upcoming & past)

  return db.query(Booking).filter(Booking.guest_id == int(guest_data['sub']))

# Guest see a detail booking
@router.get('/{booking_id}', response_model=BookingDisplay)
def view_booking(
  booking_id: int,
  guest_data = Depends(require_guest),
  db: Session = Depends(get_db)
  ):

  booking = db.query(Booking).filter(Booking.id == booking_id).first()

  if not booking:
    raise HTTPException(status_code=404, detail='Booking not found')

  return booking

# Cancel booking
@router.patch('/{booking_id}/cancel', response_model=BookingDisplay)
def cancel_booking(
  booking_id: int,
  db: Session = Depends(get_db),
  guest_data = Depends(require_guest)):
  # works only for pending and confirmed
  pass

# Confirm booking
@router.patch('/{booking_id}/confirm', response_model=BookingDisplay)
def confirm_booking(booking_id: int, guest_data):
  pass

# Get all bookings for one hotel
@router.get('hotels/{hotel_id}', response_model=list[BookingDisplay])
def view_all_hotel_bookings(
  hotel_id: int,
  token_data = Depends(require_hotel_manager)):

  pass

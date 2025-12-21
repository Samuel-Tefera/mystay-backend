from fastapi import APIRouter, Depends, HTTPException

from sqlalchemy.orm import Session

from app.core.dependencies import require_guest, require_guest_manager, require_hotel_manager
from app.database import get_db
from app.models.bookings import Booking, BookingStatus
from app.models.hotel import Hotel
from app.models.payments import Payment, PaymentMethod
from app.models.room import Room
from app.models.users import Guest
from app.schemas.bookings import BookingCreate, BookingDisplay
from app.utils.booking_services import can_manager_update_booking, can_user_update_booking, is_room_available


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

  if not booking or booking.guest_id != int(guest_data['sub']):
    raise HTTPException(status_code=400, detail='Can\'t access booking')

  return booking

# Cancel booking
@router.patch('/{booking_id}/cancel')
def cancel_booking(
  booking_id: int,
  db: Session = Depends(get_db),
  user_data = Depends(require_guest_manager)):

  booking = db.query(Booking).filter(Booking.id == booking_id).first()

  can_user_update_booking(user_data, booking, db)

  if booking.status == BookingStatus.CONFIRMED or booking.status == BookingStatus.PENDING:
    booking.status = BookingStatus.CANCELLED
    db.commit()
    db.refresh(booking)

    return {
      'message' : 'Booking has been successfully cancelled'
    }

  raise HTTPException(status_code=409, detail='Booking can not be cancelled')

# Confirm booking
@router.patch('/{booking_id}/confirm')
def confirm_booking(
  booking_id: int,
  db: Session = Depends(get_db),
  manager_data = Depends(require_hotel_manager )):

  booking = db.query(Booking).filter(Booking.id == booking_id).first()

  can_manager_update_booking(manager_data, booking, db)

  if booking.status == BookingStatus.PENDING:
    booking.status = BookingStatus.CONFIRMED
    db.commit()
    db.refresh(booking)

    return {
      'message' : 'Booking has been successfully confirmed'
    }

  raise HTTPException(status_code=409, detail='Booking can not be confirmed')

# Complete booking
@router.patch('/{booking_id}/complete')
def complete_booking(
  booking_id: int,
  db: Session = Depends(get_db),
  manager_data = Depends(require_hotel_manager)
):

  booking = db.query(Booking).filter(Booking.id == booking_id).first()

  can_manager_update_booking(manager_data, booking, db)


  if booking.status == BookingStatus.CONFIRMED:
    booking.status = BookingStatus.COMPLETED
    db.commit()
    db.refresh(booking)

    return {
      'message' : 'Booking has been successfully completed'
    }

  raise HTTPException(status_code=409, detail='Booking can not be confirmed')

# Get all bookings for one hotel
@router.get('/hotels/{hotel_id}', response_model=list[BookingDisplay])
def view_all_hotel_bookings(
  hotel_id: int,
  manager_data = Depends(require_hotel_manager),
  db: Session = Depends(get_db)):

  hotel = db.query(Hotel).filter(Hotel.id == hotel_id).first()

  if not hotel:
    raise HTTPException(status_code=404, detail='Not found')

  if hotel.manager_id != int(manager_data['sub']):
    raise HTTPException(status_code=403, detail='Not have permission to access')

  return db.query(Booking).filter(Booking.hotel_id == hotel_id)

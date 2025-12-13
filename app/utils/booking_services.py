from fastapi import HTTPException
from sqlalchemy.orm import Session

from datetime import date

from app.models.bookings import Booking
from app.models.hotel import Hotel


def is_room_available(db : Session, room_id: int, check_in , check_out):
    conflicting = db.query(Booking).filter(
        Booking.room_id == room_id,
        Booking.status.in_(["pending", "confirmed"]),
        Booking.check_in < check_out,
        Booking.check_out > check_in
    ).first()

    return not conflicting


def can_manager_update_booking(manager_data, booking, db):
    hotel = db.query(Hotel).filter(Hotel.id == booking.hotel_id).first()
    if not hotel:
        raise HTTPException(status_code=404, detail='Booking not found')
    if hotel.manager_id != int(manager_data['sub']):
        raise HTTPException(status_code=403)


def can_user_update_booking(user_data, booking, db):
    if not booking:
        raise HTTPException(status_code=404, detail='Booking not found')

    if user_data['role'] == 'guest':
        if booking.guest_id != int(user_data['sub']):
            raise HTTPException(status_code=403)

    if user_data['role'] == 'manager':
        can_manager_update_booking(user_data, booking, db)

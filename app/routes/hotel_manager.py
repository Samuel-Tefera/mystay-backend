from datetime import date, datetime, timedelta

from fastapi import APIRouter, Depends, HTTPException

from sqlalchemy import select, func, distinct
from sqlalchemy.orm import Session

from app.core.dependencies import FRONTEND_RESET_PASSWORD_URL, require_admin, require_hotel_manager
from app.core.security import create_manager_token, generate_reset_token, hash_password, hash_token, verify_password
from app.crud.users import get_all_hotel_managers, get_hotel_manager
from app.database import get_db
from app.models.bookings import Booking
from app.models.hotel import Hotel
from app.models.password_reset import PasswordResetToken
from app.models.payments import Payment, PaymentStatus
from app.models.room import Room
from app.models.users import HotelManager
from app.schemas.users import HotelManagerDisplay, HotelManagerForgetPassword, HotelManagerLogin, HotelManagerPasswordUpdate, HotelManagerResetPassword
from app.utils.email_service import send_password_reset_email


router = APIRouter(prefix='/hotelmanager', tags=['HotelManager'])

# Handle login
@router.post('/login')
def hotel_manager_login(credentials: HotelManagerLogin, db: Session = Depends(get_db)):
  manager = db.query(HotelManager).filter(HotelManager.email == credentials.email).first()

  if not manager or not verify_password(credentials.password, manager.password):
    raise HTTPException(status_code=401, detail='Invalid credentials')

  token = create_manager_token(manager)

  return {
    "access_token": token,
    "token_type": "bearer",
    "manager_id": manager.id,
    "manager_name": manager.name,
    "manager_email": manager.email,
  }


# Hotel Dashboard for Hotel Manager
@router.get('/dashboard')
def get_hotel_dashboard(
  db: Session = Depends(get_db),
  manager_data = Depends(require_hotel_manager)
):

  # Manager Hotel
  hotel = db.query(Hotel).filter(Hotel.manager_id == int(manager_data['sub'])).first()

  # Total Rooms
  stmt = select(func.count(Room.id)).where(Room.hotel_id == hotel.id)
  total_rooms = db.execute(stmt).scalar() or 0

  # Total Bookings
  stmt = select(func.count(Booking.id)).where(Booking.hotel_id == hotel.id)
  total_bookings = db.execute(stmt).scalar() or 0

  # Occupied Rooms
  today = date.today()
  occupied_rooms = db.query(
      func.count(distinct(Booking.room_id))
    ).filter(
        Booking.status == "CONFIRMED",
        Booking.check_in <= today,
        Booking.check_out > today
    ).scalar()

  # Total Sales
  stmt = select(Booking.id)
  booking_ids = db.execute(stmt).scalars().all()

  total_sales = db.query(
    func.sum(Payment.amount)
  ).filter(
    Payment.status == PaymentStatus.PAID,
    Payment.booking_id.in_(booking_ids)
  ).scalar()

  return {
    'hotels': {
      'id': hotel.id,
      'name': hotel.name
    },
    'stats': {
      'total_rooms': total_rooms,
      'total_bookings': total_bookings,
      'occupied_rooms': occupied_rooms,
      'total_sales': total_sales,
    }
  }


# Handle update password
@router.patch('/{manager_id}/update-password')
def update_password(
  manager_id: int,
  credentials: HotelManagerPasswordUpdate,
  db: Session = Depends(get_db),
  token_data = Depends(require_hotel_manager)):

  if int(token_data['sub']) != manager_id:
        raise HTTPException(status_code=403, detail='Not allowed')

  manager = db.query(HotelManager).filter(HotelManager.id == manager_id).first()

  if not manager or not verify_password(credentials.current_password, manager.password):
    raise HTTPException(status_code=401, detail='Invalid credentials')

  manager.password = hash_password(credentials.new_password)
  db.commit()
  db.refresh(manager)

  return {'message': 'Password Successfully Updated'}


@router.post('/forgot-password')
def forget_password(
  payload: HotelManagerForgetPassword,
  db: Session = Depends(get_db)
  ):
  email = payload.email

  if not email:
    raise HTTPException(status_code=400, detail="Email is required")

  manager = db.query(HotelManager).filter(HotelManager.email == email).first()

  response_message = {
      "message": "If the email exists, password reset instructions have been sent."
    }

  if not manager:
    return response_message

# Invalidate previous tokens
  db.query(PasswordResetToken).filter(
      PasswordResetToken.user_id == manager.id,
      PasswordResetToken.is_used == False
  ).update({"is_used": True})

  raw_token = generate_reset_token()
  token_hash = hash_token(raw_token)

  reset_token = PasswordResetToken(
    user_id = manager.id,
    token_hash = token_hash,
    expires_at=datetime.utcnow() + timedelta(minutes=30),
    is_used = False
  )

  db.add(reset_token)
  db.commit()

  reset_link = f"{FRONTEND_RESET_PASSWORD_URL}?token={raw_token}"

  send_password_reset_email(
    to_email=manager.email,
    reset_link=reset_link
  )

  return response_message

@router.post('/reset-password')
def reset_password(
  payload: HotelManagerResetPassword,
  db: Session = Depends(get_db)
  ):

  token_hash = hash_token(payload.token)

  reset_token = db.query(PasswordResetToken).filter(
    PasswordResetToken.token_hash == token_hash,
    PasswordResetToken.is_used == False
  ).first()

  if not reset_token:
    raise HTTPException(status_code=400, detail='Invalid or expired token')

  if reset_token.expires_at < datetime.utcnow():
    raise HTTPException(status_code=400, detail='Token has expired')

  manager = db.query(HotelManager).filter(HotelManager.id == reset_token.user_id).first()

  if not manager:
    raise HTTPException(status_code=400, detail='Invalid token')

  manager.password = hash_password(payload.new_password)

  reset_token.is_used = True

  db.commit()

  return {
    'message': 'Password has been reset successfully'
  }

# Manager profile
@router.get('/me', response_model=HotelManagerDisplay)
def manager_profile(
  token = Depends(require_hotel_manager),
  db: Session = Depends(get_db)
  ):
  manager = db.query(HotelManager).filter(HotelManager.id == int(token['sub'])).first()

  if not manager:
    raise HTTPException(status_code=404, detail='No manager found')

  return manager


# Get all managers for Admin
@router.get('/', response_model=list[HotelManagerDisplay], dependencies=[Depends(require_admin)])
def get_managers(db: Session = Depends(get_db)):
  return get_all_hotel_managers(db)

# Get one manager by ID for Admin
@router.get('/{manager_id}', response_model=HotelManagerDisplay, dependencies=[Depends(require_admin)])
def get_manager(manager_id: int, db: Session = Depends(get_db)):
  db_manager = get_hotel_manager(db, manager_id)

  if not db_manager:
    raise HTTPException(status_code=404, detail='Manager not found')

  return db_manager

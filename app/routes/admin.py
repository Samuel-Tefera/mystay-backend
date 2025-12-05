from fastapi import APIRouter, Depends, HTTPException

from sqlalchemy.orm import Session
from app.core.dependencies import require_admin

from app.core.security import create_admin_token, verify_password
from app.crud.hotel import get_hotel_application_detail
from app.database import get_db
from app.models.hotel import Hotel
from app.models.users import Admin, HotelManager
from app.schemas.users import AdminLogin
from app.core.security import hash_password
from app.utils.email_service import send_application_approved_email, send_application_rejected_email
from app.utils.utils import generate_password


router = APIRouter(prefix='/admin', tags=['Admin'])

# Handle Admin Login
@router.post('/login')
def admin_login(credentials: AdminLogin, db:Session = Depends(get_db)):
  admin = db.query(Admin).filter(Admin.email == credentials.email).first()

  if not admin or not verify_password(credentials.password, admin.password_hash):
    raise HTTPException(status_code=401, detail='Invalid credentials')

  token = create_admin_token(admin)

  return {
    "access_token": token,
    "token_type": "bearer",
    "admin_name": admin.full_name,
    "admin_email": admin.email,
    "admin_id": admin.id,
  }

# Handle approving hotel applications
@router.post('/{app_id}/approve', dependencies=[Depends(require_admin)])
def approve_application(app_id: int, db: Session = Depends(get_db)):
  db_app = get_hotel_application_detail(db, app_id)

  if not db_app:
    raise HTTPException(status_code=404, detail='Application not found')

  if db_app.status != 'pending':
      raise HTTPException(status_code=400, detail='Already processed')

  # Generate temporary password for Hotel Manager
  temp_pass = generate_password()
  hashed_pass = hash_password(temp_pass)

  # Create Hotel Manager Account
  db_manager = HotelManager(
    name = db_app.manager_name,
    email = db_app.manager_email,
    phone = db_app.manager_phone,
    password = hashed_pass,
  )

  db.add(db_manager)
  db.commit()
  db.refresh(db_manager)

  # Create Hotel
  db_hotel = Hotel(
    manager_id = db_manager.id,
    name = db_app.hotel_name,
    description = db_app.hotel_description,
    address = db_app.hotel_address,
    rating = db_app.hotel_star_rating,
    exact_location = db_app.hotel_exact_location,
  )

  db.add(db_hotel)
  db.commit()
  db.refresh(db_hotel)

  # Update application status
  db_app.status = "approved"
  db.commit()

  # Send email for Hotel manager including genrated password
  send_application_approved_email(db_manager.email, temp_pass, db_hotel.name)

  return{
    'message': 'Application approved. Manager + Hotel created',
    'manager_id': db_manager.id,
    'hotel_id': db_hotel.id
  }

# Handle hotel application rejection
@router.post('/{app_id}/reject', dependencies=[Depends(require_admin)])
def reject_application(app_id: int, db: Session = Depends(get_db)):
  db_app = get_hotel_application_detail(db, app_id)

  if not db_app:
    raise HTTPException(status_code=404, detail='Application not found')

  if db_app.status != 'pending':
      raise HTTPException(status_code=400, detail='Already processed')

  # Update application status
  db_app.status = "rejected"
  db.commit()

  # send email
  send_application_rejected_email(db_app.manager_email, db_app.hotel_name)

  return{
    'message': 'Application rejected'
  }

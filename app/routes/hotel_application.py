from fastapi import APIRouter, Depends, HTTPException

from sqlalchemy.orm import Session
from app.crud.hotel import create_new_hotel_application, get_all_hotel_applications, get_hotel_application_detail
from app.database import get_db

from app.schemas.hotel import HotelApplicationCreate, HotelApplicationDetailDisplay, HotelApplicationDisplay


router = APIRouter(prefix='/hotel/application', tags=['Hotel Application'])

# Create new hotel application
@router.post('/', response_model=HotelApplicationDetailDisplay)
def create_application(new_application: HotelApplicationCreate, db: Session = Depends(get_db)):
  return create_new_hotel_application(db, new_application)

# Get all applications
@router.get('/', response_model=list[HotelApplicationDisplay])
def get_applications(db: Session = Depends(get_db)):
  return get_all_hotel_applications(db)

# Get application detail
@router.get('/{application_id}', response_model=HotelApplicationDetailDisplay)
def get_application(application_id, db: Session = Depends(get_db)):
  db_application = get_hotel_application_detail(db, application_id)

  if not db_application:
    raise HTTPException(status_code=404, detail='Application with this id not found')

  return db_application

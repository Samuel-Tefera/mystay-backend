from fastapi import HTTPException
from sqlalchemy import or_
from sqlalchemy.orm import Session
from app.models.hotel import Hotel, HotelApplication

from app.schemas.hotel import HotelApplicationCreate, HotelUpdate


# Creating new hotel application
def create_new_hotel_application(
  db: Session,
  new_hotel_application: HotelApplicationCreate
  ):

  db_hotel_application = HotelApplication(
    manager_name = new_hotel_application.manager_name,
    manager_email = new_hotel_application.manager_email,
    manager_phone = new_hotel_application.manager_phone,

    hotel_name = new_hotel_application.hotel_name,
    hotel_address = new_hotel_application.hotel_address,
    hotel_description = new_hotel_application.hotel_description,
    hotel_star_rating = new_hotel_application.hotel_star_rating,
    hotel_exact_location = new_hotel_application.hotel_exact_location.model_dump(),
  )

  db.add(db_hotel_application)
  db.commit()
  db.refresh(db_hotel_application)

  return db_hotel_application

# Get all hotel applications
def get_all_hotel_applications(db : Session):
  return db.query(HotelApplication).all()

# Get hotel application detail
def get_hotel_application_detail(
  db: Session,
  application_id: int):

  return db.query(HotelApplication).filter(HotelApplication.id == application_id).first()

# Get all Hotels
def get_all_hotels(search: str | None, db: Session):
  query = db.query(Hotel)

  if search:
    query = query.filter(
        or_(
            Hotel.name.ilike(f"%{search}%"),
            Hotel.address.ilike(f"%{search}%"),
        )
    )

  return query.all()

# Get Hotel
def get_one_hotel(
  db: Session,
  hotel_id: int):

  return db.query(Hotel).filter(Hotel.id == hotel_id).first()

from sqlalchemy.orm import Session
from app.models.hotel import Hotel, HotelApplication

from app.schemas.hotel import HotelApplicationCreate, HotelCreate


# Creating new hotel application
def create_new_hotel_application(db: Session, new_hotel_application: HotelApplicationCreate):
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
def get_hotel_application_detail(db: Session, application_id: int):
  return db.query(HotelApplication).filter(HotelApplication.id == application_id).first()

# Creating new Hotel
def create_new_hotel(db: Session, new_hotel: HotelCreate):
  db_hotel = Hotel(
    manager_id = new_hotel.manager_id,
    name = new_hotel.name,
    description = new_hotel.description,
    address = new_hotel.address,
    rating = new_hotel.rating,
    exact_location = new_hotel.exact_location.dict(),
  )

  db.add(db_hotel)
  db.commit()
  db.refresh(db_hotel)

  return db_hotel

# Get all Hotels
def get_all_hotels(db: Session):
  return db.query(Hotel).all()

# Get Hotel
def get_one_hotel(db: Session, hotel_id: int):
  return db.query(Hotel).filter(Hotel.id == hotel_id).first()

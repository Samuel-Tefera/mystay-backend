from sqlalchemy.orm import Session
from app.models.hotel import Hotel

from app.schemas.hotel import HotelCreate


# Creating new Hotel
def create_new_hotel(db: Session, new_hotel: HotelCreate):
  db_hotel = Hotel(
    manager_id = new_hotel.manager_id,
    name = new_hotel.name,
    description = new_hotel.description,
    address = new_hotel.address,
    rating = new_hotel.rating,
    exact_location = new_hotel.exact_location.dict(),
    contact_number = new_hotel.contact_number,
    email = new_hotel.email
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

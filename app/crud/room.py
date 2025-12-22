from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy import and_
from sqlalchemy.orm import Session

from app.models.room import Room
from app.schemas.room import RoomBase


# Creating new room for Hotel
def create_new_room(hotel_id, new_room: RoomBase, image_url: str, db: Session):
  db_room = Room(
    hotel_id = hotel_id,
    room_number = new_room.room_number,
    room_type = new_room.room_type,
    price_per_night = new_room.price_per_night,
    description = new_room.description,
    bed_type = new_room.bed_type,
    image_url = image_url,
  )

  try:
    db.add(db_room)
    db.commit()
    db.refresh(db_room)
  except IntegrityError:
    db.rollback()
    raise HTTPException(
        status_code=409,
        detail='Room number already exsits for this hotel'
      )

  return db_room

# Get all rooms for one hotel
def get_all_rooms(db: Session, hotel_id: int = None):
  if not hotel_id:
    return db.query(Room).all()
  return db.query(Room).filter(Room.hotel_id == hotel_id)

# get one room
def get_one_room(hotel_id: int, room_id: int, db: Session):
  return db.query(Room).filter(and_(Room.id == room_id, Room.hotel_id == hotel_id)).first()

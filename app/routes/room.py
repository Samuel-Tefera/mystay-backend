from fastapi import APIRouter, Depends

from sqlalchemy.orm import Session
from app.crud.room import create_new_room, get_all_rooms, get_one_room

from app.schemas.room import RoomBase, RoomDisaply
from app.database import get_db


router = APIRouter(prefix='/hotels/{hotel_id}/rooms', tags=['Rooms'])

# Create new room for Hotel
@router.post('/', response_model=RoomDisaply)
def create_room(hotel_id, new_room: RoomBase, db: Session = Depends(get_db)):
  return create_new_room(hotel_id, new_room, db)

# Get all rooms for one Hotel
@router.get('/', response_model=list[RoomDisaply])
def get_rooms(hotel_id, db: Session = Depends(get_db)):
  return get_all_rooms(hotel_id, db)

# Get all specific room
@router.get('/{room_id}', response_model=RoomDisaply)
def get_room(hotel_id, room_id, db: Session = Depends(get_db)):
  return get_one_room(hotel_id, room_id, db)
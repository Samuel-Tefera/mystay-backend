from fastapi import APIRouter, Depends, HTTPException

from sqlalchemy.orm import Session
from app.core.dependencies import require_hotel_manager
from app.crud.room import create_new_room, get_all_rooms, get_one_room
from app.models.hotel import Hotel
from app.models.room import Room

from app.schemas.room import RoomBase, RoomDisaply
from app.database import get_db


router = APIRouter(prefix='/hotels', tags=['Rooms'])

# Get all rooms
@router.get('/rooms', response_model=list[RoomDisaply])
def get_rooms(db: Session = Depends(get_db)):
  return get_all_rooms(db)

# Get all rooms for one Hotel
@router.get('/{hotel_id}/rooms', response_model=list[RoomDisaply])
def get_rooms_for_hotel(hotel_id, db: Session = Depends(get_db)):
  return get_all_rooms(db, hotel_id)

# Get specific room
@router.get('/{hotel_id}/rooms/{room_id}', response_model=RoomDisaply)
def get_room(hotel_id, room_id, db: Session = Depends(get_db)):
  return get_one_room(hotel_id, room_id, db)

# Create new room for Hotel
@router.post('/{hotel_id}/rooms', response_model=RoomDisaply, dependencies=[Depends(require_hotel_manager)])
def create_room(hotel_id, new_room: RoomBase, db: Session = Depends(get_db)):
  return create_new_room(hotel_id, new_room, db)

# Delete room
@router.delete('/rooms/{room_id}')
def delete_room(
  room_id: int,
  db: Session = Depends(get_db),
  token_data = Depends(require_hotel_manager)):

  room = db.query(Room).filter(Room.id == room_id).first()
  if not room:
    raise HTTPException(status_code=404, detail='Room Not found')

  # Check delete is by right hotel owner
  hotel = db.query(Hotel).filter(Hotel.id == room.hotel_id).first()

  if hotel.manager_id != int(token_data['sub']):
    raise HTTPException(status_code=403, detail='Not allowed')

  db.delete(room)
  db.commit()
  return {
    'message': 'Room successfully removed.'
  }

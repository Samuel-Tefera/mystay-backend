from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile

from sqlalchemy.orm import Session

from app.core.dependencies import require_hotel_manager
from app.crud.room import create_new_room, get_all_rooms, get_one_room
from app.models.hotel import Hotel
from app.models.room import BedType, Room, RoomType
from app.schemas.room import RoomBase, RoomDisaply, RoomUpdate
from app.database import get_db
from app.utils.room_service import save_room_image


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
def create_room(
  hotel_id: int,
  room_number: str = Form(...),
  room_type: RoomType = Form(...),
  price_per_night: float = Form(...),
  description: str = Form(...),
  bed_type: BedType = Form(...),
  image: UploadFile = File(...),
  db: Session = Depends(get_db)
  ):

  new_room = RoomBase(
    room_number=room_number,
    room_type=room_type,
    price_per_night=price_per_night,
    description=description,
    bed_type=bed_type,
    )

  image_url = save_room_image(image)

  return create_new_room(hotel_id, new_room, image_url, db)

# Update room
@router.patch('/{hotel_id}/rooms/{room_id}')
def update_room(
  room_id: int,
  room_update: RoomUpdate,
  db: Session = Depends(get_db),
  token_data = Depends(require_hotel_manager)
):

  room = db.query(Room).filter(Room.id == room_id).first()

  if not room:
    raise HTTPException(status_code=404, detail='Room not found')

  # Check update is by right hotel owner
  hotel = db.query(Hotel).filter(Hotel.id == room.hotel_id).first()

  if hotel.manager_id != int(token_data['sub']):
    raise HTTPException(status_code=403, detail='Not allowed')

  update_data = room_update.model_dump(exclude_unset=True)

  for key, value in update_data.items():
    setattr(room, key, value)

  db.commit()
  db.refresh(room)
  return room

# Delete room
@router.delete('/{hotel_id}/rooms/{room_id}')
def delete_room(
  room_id: int,
  db: Session = Depends(get_db),
  token_data = Depends(require_hotel_manager)
  ):

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

from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Query

from sqlalchemy.orm import Session

from app.core.dependencies import require_hotel_manager
from app.database import get_db
from app.models.hotel import Hotel
from app.schemas.hotel import HotelDisplay, HotelDisplayDetail, HotelUpdate
from app.crud.hotel import get_all_hotels, get_one_hotel


router = APIRouter(prefix='/hotels', tags=['Hotels'])

# Get all Hotels
@router.get('/', response_model=list[HotelDisplay])
def get_hotels(
  search: str | None = Query(
    default=None,
    min_length=2,
    description='Search by hotel name or address'
  ),
  db: Session = Depends(get_db)):
  return get_all_hotels(search, db)

# Get one Hotel by ID
@router.get('/{hotel_id}', response_model=HotelDisplayDetail)
def get_hotel(hotel_id: int, db: Session = Depends(get_db)):
  db_hotel = get_one_hotel(db, hotel_id)

  if not db_hotel:
    raise HTTPException(status_code=404, detail='Hotel not found')

  return db_hotel

# Update hotel
@router.patch('/{hotel_id}', response_model=HotelDisplay)
def update_hotel(
  hotel_id: int,
  hotel_update: HotelUpdate,
  db: Session = Depends(get_db),
  token_data = Depends(require_hotel_manager)):

  hotel = db.query(Hotel).filter(Hotel.id == hotel_id).first()

  if not hotel:
    raise HTTPException(status_code=404, detail='Hotel not found.')

  if hotel.manager_id != int(token_data['sub']):
    raise HTTPException(status_code=403, detail='Not allowed')

  update_data = hotel_update.model_dump(exclude_unset=True)

  for key, value in update_data.items():
      setattr(hotel, key, value)

  db.commit()
  db.refresh(hotel)
  return hotel

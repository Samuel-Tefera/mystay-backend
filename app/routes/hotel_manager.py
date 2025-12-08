from fastapi import APIRouter, Depends, HTTPException

from sqlalchemy.orm import Session

from app.core.dependencies import require_admin, require_hotel_manager
from app.core.security import create_manager_token, hash_password, verify_password
from app.crud.users import get_all_hotel_managers, get_hotel_manager
from app.database import get_db
from app.models.users import HotelManager
from app.schemas.users import HotelManagerDisplay, HotelManagerLogin, HotelManagerPasswordUpdate


router = APIRouter(prefix='/hotelmanager', tags=['HotelManager'])

# Handle login
@router.post('/login')
def hotel_manager_login(credentials: HotelManagerLogin, db: Session = Depends(get_db)):
  manager = db.query(HotelManager).filter(HotelManager.email == credentials.email).first()

  if not manager or not verify_password(credentials.password, manager.password):
    raise HTTPException(status_code=401, detail='Invalid credentials')

  token = create_manager_token(manager)

  return {
    "access_token": token,
    "token_type": "bearer",
    "manager_id": manager.id,
    "manager_name": manager.name,
    "manager_email": manager.email,
  }


# Handle update password
@router.patch('/{manager_id}/update-password')
def update_password(
  manager_id: int,
  credentials: HotelManagerPasswordUpdate,
  db: Session = Depends(get_db),
  token_data = Depends(require_hotel_manager)):

  if int(token_data['sub']) != manager_id:
        raise HTTPException(status_code=403, detail='Not allowed')

  manager = db.query(HotelManager).filter(HotelManager.id == manager_id).first()

  if not manager or not verify_password(credentials.current_password, manager.password):
    raise HTTPException(status_code=401, detail='Invalid credentials')

  manager.password = hash_password(credentials.new_password)
  db.commit()
  db.refresh(manager)

  return {'message': 'Password Successfully Updated'}


# Get all managers for Admin
@router.get('/', response_model=list[HotelManagerDisplay], dependencies=[Depends(require_admin)])
def get_managers(db: Session = Depends(get_db)):
  return get_all_hotel_managers(db)

# Get one manager by ID for Admin
@router.get('/{manager_id}', response_model=HotelManagerDisplay, dependencies=[Depends(require_admin)])
def get_manager(manager_id: int, db: Session = Depends(get_db)):
  db_manager = get_hotel_manager(db, manager_id)

  if not db_manager:
    raise HTTPException(status_code=404, detail='Manager not found')

  return db_manager

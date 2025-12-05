from fastapi import Depends, HTTPException
from app.core.security import decode_token, admin_oauth2_scheme, manager_oauth2_scheme

def require_admin(token: str = Depends(admin_oauth2_scheme)):
    payload = decode_token(token)

    if payload.get('role') != 'admin':
        raise HTTPException(status_code=403, detail='Admins only')

    return payload

def require_hotel_manager(token: str = Depends(manager_oauth2_scheme)):
    payload = decode_token(token)

    if payload.get('role') != 'manager':
        raise HTTPException(status_code=403, detail="Hotel Mangers only")

    return payload

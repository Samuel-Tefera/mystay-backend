import os
from dotenv import load_dotenv
from fastapi import Depends, HTTPException

from app.core.security import decode_token, oauth2_scheme

def require_admin(token: str = Depends(oauth2_scheme)):
    '''Allow access if user is Admin'''
    payload = decode_token(token)

    if payload.get('role') != 'admin':
        raise HTTPException(status_code=403, detail='Admins only')

    return payload

def require_hotel_manager(token: str = Depends(oauth2_scheme)):
    '''Allow access if user is Hotel Manager'''
    payload = decode_token(token)

    if payload.get('role') != 'manager':
        raise HTTPException(status_code=403, detail='Hotel Mangers only')

    return payload

def require_guest(token: str = Depends(oauth2_scheme)):
    '''Allow access if user is Guest'''
    payload = decode_token(token)

    if payload.get('role') != 'guest':
        raise HTTPException(status_code=403, detail='Guest only')

    return payload

def require_guest_manager(
   token = Depends(oauth2_scheme, use_cache=False)
):
    ''' Allow access if user is EITHER a manager OR a guest '''

    payload = decode_token(token)

    if payload.get('role') == 'guest' or payload.get('role') == 'manager':
        return payload

    raise HTTPException(
        status_code=401,
        detail='Guest or Hotel Manager authentication required',
    )

load_dotenv()
FRONTEND_RESET_PASSWORD_URL=os.getenv('FRONTEND_RESET_PASSWORD_URL')


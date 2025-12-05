from fastapi import Depends, HTTPException
from app.core.security import decode_token, oauth2_scheme

def require_admin(token: str = Depends(oauth2_scheme)):
    payload = decode_token(token)

    if payload.get("role") != "admin":
        raise HTTPException(status_code=403, detail="Admins only")

    return payload

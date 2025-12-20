import hashlib
import secrets
from fastapi import HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
from datetime import datetime, timedelta
from jose import JWTError, jwt
import os

# Password Hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24  # 1 day
SECRET_KEY = os.getenv("ADMIN_SECRET_KEY", "supersecret123")
ALGORITHM = "HS256"

# Token generator
def create_access_token(data: dict, expires_minutes: int = ACCESS_TOKEN_EXPIRE_MINUTES):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=expires_minutes)
    to_encode.update({"exp": expire})

    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


# JWT Token for Admin
def create_admin_token(admin):
    return create_access_token({
        'sub': str(admin.id),
        'email': admin.email,
        'role': 'admin',
    })

# JWT Token for HotelManager
def create_manager_token(manager):
    return create_access_token({
        'sub': str(manager.id),
        'email': manager.email,
        'role': 'manager',
    })

# JWT Token for Guest
def create_guest_token(guest):
    return create_access_token({
    'sub': str(guest.id),
    'email': guest.email,
    'role': 'guest',
})

# OAuth2 scheme to extract "Authorization: Bearer <token>"
oauth2_scheme = OAuth2PasswordBearer(tokenUrl='/api/auth/login')

# Decode JWT
def decode_token(token: str):
    try:
        return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
        )


# Generate token for manager to reset password
def generate_reset_token() -> str:
    return secrets.token_urlsafe(32)

def hash_token(token: str) -> str:
    return hashlib.sha256(token.encode()).hexdigest()

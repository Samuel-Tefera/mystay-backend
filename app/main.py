from fastapi import FastAPI
from starlette.middleware.sessions import SessionMiddleware
import os

from app.routes import hotel_manager, hotel, room, auth

app = FastAPI(title='MyStay API')

app.add_middleware(
    SessionMiddleware,
    secret_key=os.getenv("SESSION_SECRET", "super-secret-session-key"),
)

app.include_router(hotel_manager.router, prefix='/api')
app.include_router(hotel.router, prefix='/api')
app.include_router(room.router, prefix='/api')
app.include_router(auth.router, prefix='/api')

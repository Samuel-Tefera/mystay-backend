from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware

from starlette.middleware.sessions import SessionMiddleware

import os

from app.routes import guest, hotel_application, hotel_manager, hotel, room, auth, admin, bookings

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        # actual IP
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="MyStay API",
        version="1.0.0",
        routes=app.routes,
    )
    # Change OAuth2PasswordBearer to simple bearer token in docs
    openapi_schema["components"]["securitySchemes"]["OAuth2PasswordBearer"] = {
        "type": "http",
        "scheme": "bearer",
        "bearerFormat": "JWT"
    }
    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi


app.add_middleware(
    SessionMiddleware,
    secret_key=os.getenv("SESSION_SECRET", "super-secret-session-key"),
)

app.mount("/uploads", StaticFiles(directory="app/uploads"), name="uploads")

app.include_router(admin.router, prefix='/api')
app.include_router(hotel_application.router, prefix='/api')
app.include_router(hotel_manager.router, prefix='/api')
app.include_router(guest.router, prefix='/api')
app.include_router(room.router, prefix='/api')
app.include_router(hotel.router, prefix='/api')
app.include_router(bookings.router, prefix='/api')
app.include_router(auth.router, prefix='/api')

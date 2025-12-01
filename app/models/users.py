from datetime import datetime
from sqlalchemy import Column, DateTime, Integer, String, Boolean
from sqlalchemy.orm import relationship

from app.database import Base


class Admin(Base):
  """Admin user model"""
  __tablename__ = 'admins'

  id = Column(Integer, primary_key=True, index=True)
  email = Column(String, unique=True, nullable=False)
  password_hash = Column(String, nullable=False)
  full_name = Column(String, nullable=False)
  created_at = Column(DateTime, default=datetime.utcnow)


class HotelManager(Base):
    """Hotel Manager user Model"""
    __tablename__ = "hotel_managers"

    id = Column(Integer, primary_key=True, index=True)

    name = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True, index=True)
    phone = Column(String, nullable=True)

    is_approved = Column(Boolean, default=False) # Magic link authentication

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    last_login = Column(DateTime, nullable=True)

    # Relation to hotel
    hotel = relationship("Hotel", back_populates="manager")


# Guest User
class Guest(Base):
  '''Guest User Model'''
  __tablename__ = 'guest'

  id = Column(Integer, primary_key=True, index=True)
  google_id = Column(String, unique=True)
  email = Column(String, unique=True)
  full_name = Column(String, nullable=True)
  avater_url = Column(String, nullable=True)
  created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

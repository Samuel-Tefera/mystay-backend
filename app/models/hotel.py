from sqlalchemy import JSON, Column, Float, ForeignKey, Integer, String, DateTime, Enum as SQLEnum
from sqlalchemy.orm import relationship

from datetime import datetime
from enum import Enum

from app.database import Base


class ApplicationStatus(str, Enum):
  PENDING = 'pending'
  APPROVED = 'approved'
  REJECTED = 'rejected'


class HotelApplication(Base):
    __tablename__ = "hotel_applications"

    id = Column(Integer, primary_key=True, index=True)

    # Manager Info
    manager_name = Column(String, nullable=False)
    manager_email = Column(String, nullable=False)
    manager_phone = Column(String, nullable=True)

    # Hotel Info
    hotel_name = Column(String, nullable=False)
    hotel_description = Column(String, nullable=True)
    hotel_address = Column(String, nullable=False)
    hotel_star_rating = Column(Integer, nullable=True)
    hotel_exact_location = Column(JSON, nullable=False)

    status = Column(SQLEnum(ApplicationStatus), default=ApplicationStatus.PENDING)

    created_at = Column(DateTime, default=datetime.utcnow)


class Hotel(Base):
  __tablename__ = 'hotels'

  id = Column(Integer, primary_key=True, index=True)
  name = Column(String(255), nullable=False)
  description = Column(String, nullable=True)
  address = Column(String, nullable=False)
  rating = Column(Float, default=0.0)
  exact_location = Column(JSON, nullable=False)

  manager_id = Column(Integer, ForeignKey('hotel_managers.id'), unique=True)
  manager = relationship('HotelManager', back_populates='hotel')

  rooms = relationship('Room', back_populates='hotel', cascade='all, delete-orphan')

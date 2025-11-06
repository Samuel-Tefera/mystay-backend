from pydantic import BaseModel


# Input Schema Hotel Manager
class HotelManagerCreate(BaseModel):
  name: str
  email: str
  phone: str | None = None
  password: str | None = None

# Output Schema Hotel Manager
class HotelMangerDisplay(BaseModel):
  id: int
  name: str
  email: str
  phone: str | None = None

  class Config:
    orm_mode = True
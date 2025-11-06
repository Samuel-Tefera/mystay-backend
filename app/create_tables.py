from app.database import Base, engine
from app.models.users import HotelManager

print("Creating tables in database...")
Base.metadata.create_all(bind=engine)
print("Tables created successfully!")

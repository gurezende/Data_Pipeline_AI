## Script to connect to the PostgreSQL database flights ##

# Imports
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.orm import declarative_base
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
DB_HOST = os.getenv("DB_HOST")
DB_NAME = os.getenv("DB_NAME") 
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")

# Update the DATABASE_URL with your actual PostgreSQL credentials
DATABASE_URL = os.getenv("DATABASE_URL", f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}")

# Create the engine for postgresql
engine = create_engine(DATABASE_URL)

# Create the local session
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# Manage the database

# Create the base class
Base = declarative_base()

# Creating a model for the flights table
class FlightPrices(Base):
    __tablename__ = "flight_prices"
    
    # Table columns
    id = Column(Integer, primary_key=True, index=True, autoincrement="auto")
    dt = Column(String, index=True)
    depart_city = Column(String)
    depart_time = Column(String)
    city_arrival = Column(String)
    time_arrival = Column(String)
    flight_number = Column(String)
    n_stops = Column(String)
    flight_lengths = Column(Float)
    ticket_prices = Column(Float, default=0)
    days_before_flight = Column(Integer)
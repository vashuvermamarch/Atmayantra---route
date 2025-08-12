from sqlalchemy import Column, Integer, String, Enum, Date
from sqlalchemy import Column, Integer, String, Date
from sqlalchemy.ext.declarative import declarative_base
from app.database import Base
import enum


Base = declarative_base()

class UserType(str, enum.Enum):
    USER = "User"
    YOGA_INSTRUCTOR = "Yoga Trainer"
    YOGA_DOCTOR = "Yoga Doctor"
    PHYSIOTHERAPIST = "Physiotherapist"

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    phone_number = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    user_type = Column(Enum(UserType), nullable=False)

class Contact(Base):
    __tablename__ = "contacts"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, nullable=False)
    phone_no = Column(String, unique=True, nullable=False)
    message = Column(String, nullable=False)

class PersonalDetail(Base):
    __tablename__ = "personal_details"
    id = Column(Integer, primary_key=True)
    phone_no = Column(String, unique=True)
    full_name = Column(String)
    dob = Column(Date)
    age = Column(Integer)  # <---- This must exist in your DB table
    gender = Column(String)
    email = Column(String)
    address = Column(String)
    photo_path = Column(String)

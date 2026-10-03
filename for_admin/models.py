from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, DateTime, Text
from sqlalchemy.orm import relationship
from datetime import datetime
from database import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False, index=True)
    password_hash = Column(String, nullable=False)
    role = Column(String, default="USER")
    branch = Column(String, nullable=True)
    year = Column(Integer, nullable=True)
    status = Column(String, default="ACTIVE")
    created_at = Column(DateTime, default=datetime.utcnow)
    organizer = relationship("Organizer", back_populates="user", uselist=False)

class Organizer(Base):
    __tablename__ = "organizers"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    organization_name = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    website = Column(String, nullable=True)
    verification_status = Column(String, default="PENDING")
    created_at = Column(DateTime, default=datetime.utcnow)
    user = relationship("User", back_populates="organizer")
    events = relationship("Event", back_populates="organizer")

class Event(Base):
    __tablename__ = "events"
    id = Column(Integer, primary_key=True, index=True)
    organizer_id = Column(Integer, ForeignKey("organizers.id"), nullable=False)
    title = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    domain = Column(String, nullable=True)
    category = Column(String, nullable=True)
    mode = Column(String, nullable=True)
    start_date = Column(String, nullable=True)
    end_date = Column(String, nullable=True)
    deadline = Column(String, nullable=True)
    location = Column(String, nullable=True)
    prize_money = Column(Integer, default=0)
    application_fee = Column(Integer, default=0)
    certificate_available = Column(Boolean, default=False)
    team_required = Column(Boolean, default=False)
    eligibility = Column(Text, nullable=True)
    status = Column(String, default="PENDING")
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    organizer = relationship("Organizer", back_populates="events")

from sqlalchemy import Boolean, Column, DateTime, String
from sqlalchemy.sql import func
from uuid import uuid4

from app.db.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(String, primary_key=True, default=lambda: str(uuid4()))

    username = Column(String, unique=True, nullable=False)

    phone_number = Column(String, unique=True, nullable=False)

    display_name = Column(String, nullable=False)

    avatar_url = Column(String, nullable=True)

    is_online = Column(Boolean, default=False)

    last_seen = Column(DateTime(timezone=True), nullable=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
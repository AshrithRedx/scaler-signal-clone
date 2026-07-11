from sqlalchemy import Column, DateTime, ForeignKey, String
from sqlalchemy.sql import func
from uuid import uuid4

from app.db.database import Base


class Session(Base):
    __tablename__ = "sessions"

    id = Column(
        String,
        primary_key=True,
        default=lambda: str(uuid4())
    )

    user_id = Column(
        String,
        ForeignKey("users.id")
    )

    token = Column(
        String,
        unique=True
    )

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )
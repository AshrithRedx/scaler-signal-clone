from sqlalchemy import Column, DateTime, ForeignKey, String, Text
from sqlalchemy.sql import func
from uuid import uuid4

from app.db.database import Base


class Message(Base):
    __tablename__ = "messages"

    id = Column(
        String,
        primary_key=True,
        default=lambda: str(uuid4())
    )

    conversation_id = Column(
        String,
        ForeignKey("conversations.id")
    )

    sender_id = Column(
        String,
        ForeignKey("users.id")
    )

    content = Column(Text)

    status = Column(
        String,
        default="sent"
    )

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )
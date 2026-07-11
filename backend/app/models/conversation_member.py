from sqlalchemy import Boolean, Column, DateTime, ForeignKey, String
from sqlalchemy.sql import func

from app.db.database import Base


class ConversationMember(Base):
    __tablename__ = "conversation_members"

    conversation_id = Column(
        String,
        ForeignKey("conversations.id"),
        primary_key=True
    )

    user_id = Column(
        String,
        ForeignKey("users.id"),
        primary_key=True
    )

    is_admin = Column(
        Boolean,
        default=False
    )

    joined_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )
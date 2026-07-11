from datetime import datetime

from pydantic import BaseModel


class MessageCreate(BaseModel):
    conversation_id: str
    sender_id: str
    content: str


class MessageResponse(BaseModel):
    id: str
    conversation_id: str
    sender_id: str
    content: str
    status: str
    created_at: datetime

    class Config:
        from_attributes = True
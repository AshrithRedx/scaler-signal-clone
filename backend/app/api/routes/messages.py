from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.schemas.message import MessageCreate, MessageResponse
from app.services.message_service import (
    send_message,
    get_conversation_messages,
)

router = APIRouter(
    prefix="/messages",
    tags=["Messages"],
)


@router.post("/", response_model=MessageResponse)
def create_message(
    request: MessageCreate,
    db: Session = Depends(get_db),
):
    return send_message(
        db,
        request.conversation_id,
        request.sender_id,
        request.content,
    )


@router.get("/{conversation_id}", response_model=list[MessageResponse])
def list_messages(
    conversation_id: str,
    db: Session = Depends(get_db),
):
    return get_conversation_messages(
        db,
        conversation_id,
    )
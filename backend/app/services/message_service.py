from sqlalchemy.orm import Session

from app.models.message import Message


def send_message(
    db: Session,
    conversation_id: str,
    sender_id: str,
    content: str,
):
    message = Message(
        conversation_id=conversation_id,
        sender_id=sender_id,
        content=content,
        status="sent",
    )

    db.add(message)
    db.commit()
    db.refresh(message)

    return message


def get_conversation_messages(
    db: Session,
    conversation_id: str,
):
    return (
        db.query(Message)
        .filter(Message.conversation_id == conversation_id)
        .order_by(Message.created_at.asc())
        .all()
    )
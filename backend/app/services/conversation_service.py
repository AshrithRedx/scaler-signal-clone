from sqlalchemy.orm import Session

from app.models.conversation import Conversation
from app.models.conversation_member import ConversationMember
from app.models.conversation_member import ConversationMember

def create_conversation(
    db: Session,
    is_group: bool,
    name: str | None,
    avatar_url: str | None,
    created_by: str,
    member_ids: list[str],
):

    conversation = Conversation(
        is_group=is_group,
        name=name,
        avatar_url=avatar_url,
        created_by=created_by,
    )

    db.add(conversation)
    db.flush()

    # Add creator
    db.add(
        ConversationMember(
            conversation_id=conversation.id,
            user_id=created_by,
            is_admin=True,
        )
    )

    # Add remaining members
    for member_id in member_ids:

        if member_id == created_by:
            continue

        db.add(
            ConversationMember(
                conversation_id=conversation.id,
                user_id=member_id,
            )
        )

    db.commit()
    db.refresh(conversation)

    return conversation


def get_conversation(
    db: Session,
    conversation_id: str,
):

    return (
        db.query(Conversation)
        .filter(Conversation.id == conversation_id)
        .first()
    )


def get_all_conversations(
    db: Session,
):

    return db.query(Conversation).all()


def add_member(
    db: Session,
    conversation_id: str,
    user_id: str,
):

    member = ConversationMember(
        conversation_id=conversation_id,
        user_id=user_id,
    )

    db.add(member)
    db.commit()

    return member

def get_user_conversations(
    db: Session,
    user_id: str,
):
    return (
        db.query(Conversation)
        .join(
            ConversationMember,
            Conversation.id == ConversationMember.conversation_id,
        )
        .filter(
            ConversationMember.user_id == user_id
        )
        .all()
    )
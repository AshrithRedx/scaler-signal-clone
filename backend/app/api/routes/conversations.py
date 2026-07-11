from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.schemas.conversation import (
    ConversationCreate,
    ConversationResponse,
    AddMemberRequest,
)
from app.services.conversation_service import (
    create_conversation,
    get_conversation,
    get_user_conversations,
    add_member,
)

router = APIRouter(
    prefix="/conversations",
    tags=["Conversations"],
)


@router.post("/", response_model=ConversationResponse)
def create_new_conversation(
    request: ConversationCreate,
    db: Session = Depends(get_db),
):
    return create_conversation(
        db=db,
        is_group=request.is_group,
        name=request.name,
        avatar_url=request.avatar_url,
        created_by=request.created_by,
        member_ids=request.member_ids,
    )


@router.get("/{conversation_id}", response_model=ConversationResponse)
def get_single_conversation(
    conversation_id: str,
    db: Session = Depends(get_db),
):
    conversation = get_conversation(db, conversation_id)

    if conversation is None:
        raise HTTPException(
            status_code=404,
            detail="Conversation not found",
        )

    return conversation


@router.get("/", response_model=list[ConversationResponse])
def list_user_conversations(
    user_id: str,
    db: Session = Depends(get_db),
):
    return get_user_conversations(
        db,
        user_id,
    )


@router.post("/{conversation_id}/members")
def add_conversation_member(
    conversation_id: str,
    request: AddMemberRequest,
    db: Session = Depends(get_db),
):
    add_member(
        db,
        conversation_id,
        request.user_id,
    )

    return {
        "message": "Member added successfully"
    }
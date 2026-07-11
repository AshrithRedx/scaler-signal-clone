from pydantic import BaseModel
from typing import List


class ConversationCreate(BaseModel):
    is_group: bool = False
    name: str | None = None
    avatar_url: str | None = None
    created_by: str
    member_ids: List[str]


class ConversationResponse(BaseModel):
    id: str
    is_group: bool
    name: str | None
    avatar_url: str | None
    created_by: str

    class Config:
        from_attributes = True


class AddMemberRequest(BaseModel):
    user_id: str
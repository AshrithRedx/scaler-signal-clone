from pydantic import BaseModel


class UserCreate(BaseModel):
    username: str
    phone_number: str
    display_name: str
    avatar_url: str | None = None


class UserResponse(BaseModel):
    id: str
    username: str
    phone_number: str
    display_name: str
    avatar_url: str | None

    class Config:
        from_attributes = True
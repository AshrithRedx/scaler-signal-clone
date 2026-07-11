from pydantic import BaseModel


class RegisterRequest(BaseModel):
    username: str
    phone_number: str
    display_name: str
    avatar_url: str | None = None


class LoginRequest(BaseModel):
    phone_number: str


class VerifyOTPRequest(BaseModel):
    phone_number: str
    otp: str


class LoginResponse(BaseModel):
    message: str


class VerifyOTPResponse(BaseModel):
    token: str
    user_id: str
    username: str
    display_name: str
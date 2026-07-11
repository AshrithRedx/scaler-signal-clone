from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.schemas.auth import (
    LoginRequest,
    LoginResponse,
    VerifyOTPRequest,
    VerifyOTPResponse,
)
from app.services.auth_service import (
    login,
    verify_otp,
    logout,
)

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"],
)


@router.post("/login", response_model=LoginResponse)
def login_user(
    request: LoginRequest,
    db: Session = Depends(get_db),
):
    result = login(db, request.phone_number)

    if result is None:
        raise HTTPException(
            status_code=404,
            detail="User not found",
        )

    return LoginResponse(
        message=result["message"]
    )


@router.post("/verify-otp", response_model=VerifyOTPResponse)
def verify_user_otp(
    request: VerifyOTPRequest,
    db: Session = Depends(get_db),
):
    result = verify_otp(
        db,
        request.phone_number,
        request.otp,
    )

    if result is None:
        raise HTTPException(
            status_code=401,
            detail="Invalid OTP",
        )

    user = result["user"]

    return VerifyOTPResponse(
        token=result["token"],
        user_id=user.id,
        username=user.username,
        display_name=user.display_name,
    )


@router.post("/logout")
def logout_user(
    token: str,
    db: Session = Depends(get_db),
):
    logout(db, token)

    return {
        "message": "Logged out successfully"
    }
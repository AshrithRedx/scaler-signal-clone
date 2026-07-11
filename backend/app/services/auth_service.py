import secrets
from sqlalchemy.orm import Session

from app.models.session import Session as UserSession
from app.services.user_service import get_user_by_phone


MOCK_OTP = "123456"


def login(db: Session, phone_number: str):
    """
    Checks whether the user exists.
    In a real application this would send an OTP.
    """

    user = get_user_by_phone(db, phone_number)

    if user is None:
        return None

    return {
        "message": "OTP sent successfully.",
        "otp": MOCK_OTP
    }


def verify_otp(db: Session, phone_number: str, otp: str):

    if otp != MOCK_OTP:
        return None

    user = get_user_by_phone(db, phone_number)

    if user is None:
        return None

    token = secrets.token_hex(32)

    session = UserSession(
        user_id=user.id,
        token=token
    )

    db.add(session)
    db.commit()

    return {
        "token": token,
        "user": user
    }


def logout(db: Session, token: str):

    session = (
        db.query(UserSession)
        .filter(UserSession.token == token)
        .first()
    )

    if session:
        db.delete(session)
        db.commit()

    return True
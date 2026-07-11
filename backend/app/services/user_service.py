from sqlalchemy.orm import Session

from app.models.user import User


def create_user(
    db: Session,
    username: str,
    phone_number: str,
    display_name: str,
    avatar_url: str | None = None,
):
    user = User(
        username=username,
        phone_number=phone_number,
        display_name=display_name,
        avatar_url=avatar_url,
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    return user


def get_user_by_phone(db: Session, phone_number: str):
    return (
        db.query(User)
        .filter(User.phone_number == phone_number)
        .first()
    )


def get_user_by_username(db: Session, username: str):
    return (
        db.query(User)
        .filter(User.username == username)
        .first()
    )


def get_user_by_id(db: Session, user_id: str):
    return (
        db.query(User)
        .filter(User.id == user_id)
        .first()
    )


def get_all_users(db: Session):
    return db.query(User).all()
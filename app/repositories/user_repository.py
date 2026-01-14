from sqlalchemy.orm import Session
from app.models import models


def get_user_by_username(db: Session, username: str) -> models.User | None:
    return db.query(models.User).filter(models.User.username == username).first()


def get_user_by_id(db: Session, user_id: int) -> models.User | None:
    return db.query(models.User).filter(models.User.id == user_id).first()


def create_user(db: Session, username: str, email: str | None, hashed_password: str, role: str = "SECRETARIA") -> models.User:
    # ensure role is stored as string
    role_str = role.value if hasattr(role, "value") else str(role)
    user = models.User(username=username, email=email, hashed_password=hashed_password, role=role_str)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

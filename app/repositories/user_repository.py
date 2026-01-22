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

def update_user_password(db: Session, username: str, new_hashed_password: str) -> models.User | None:
    user = get_user_by_username(db, username)
    if user:
        user.hashed_password = new_hashed_password
        db.commit()
        db.refresh(user)
        return user
    return None

# obtenr todos los usuarios
def get_all_users(db: Session) -> list[models.User]:
    return db.query(models.User).all()

# cambiar rol de usuario
def change_user_role(db: Session, username: str, new_role: str) -> models.User | None:
    user = get_user_by_username(db, username)
    if user:
        user.role = new_role
        db.commit()
        db.refresh(user)
        return user
    return None

# cambiar estado activo de usuario
def toggle_user_active_status(db: Session, username: str) -> models.User | None:
    user = get_user_by_username(db, username)
    if user:
        user.is_active = not user.is_active
        db.commit()
        db.refresh(user)
        return user
    return None

# cambiar email de usuario
def change_user_email(db: Session, username: str, new_email: str) -> models.User | None:
    user = get_user_by_username(db, username)
    if user:
        user.email = new_email
        db.commit()
        db.refresh(user)
        return user
    return None

# obtener carrera que gestiona un usuario (si es jefe de carrera)
def get_degree_managed_by_user(db: Session, user_id: int) -> models.Degree | None:
    return db.query(models.Degree).filter(models.Degree.jefe_carrera_user_id == user_id).first()

# obtener jefes de carrera
def get_jefes_carrera(db: Session) -> list[models.User]:
    return db.query(models.User).filter(models.User.role == "JEFE_CARRERA").all()

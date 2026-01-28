from datetime import timedelta
from typing import Optional, List
from sqlalchemy.orm import Session

from app.schemas.user_schemas import UserCreate
from app.core.security import hash_password, verify_password, create_access_token
from app.repositories import user_repository
from app.models.models import User


def register_user(db: Session, user: UserCreate) -> User:
    """Registra un nuevo usuario"""
    existing_user = user_repository.get_user_by_username(db, user.username)
    if existing_user:
        raise ValueError("El nombre de usuario ya está en uso")
    
    existing_email = user_repository.get_user_by_email(db, user.email)
    if existing_email:
        raise ValueError("El email ya está en uso")
    
    return user_repository.create_user(db, user.username, user.email, user.password, user.role)


def authenticate_user(db: Session, username: str, password: str) -> Optional[User]:
    """Autentica un usuario verificando sus credenciales"""
    user = user_repository.get_user_by_username(db, username)
    
    if not user or not verify_password(password, user.hashed_password) or not user.is_active:
        return None
    
    return user


def create_token_for_user(user: User, expires_delta: Optional[timedelta] = None) -> str:
    """Crea un token JWT para el usuario"""
    return create_access_token(
        data={"sub": user.username, "role": user.role},
        expires_delta=expires_delta
    )


def get_user_info(db: Session, user_id: int) -> Optional[User]:
    """Obtiene la información de un usuario"""
    return user_repository.get_user_by_id(db, user_id)


def update_user_info(db: Session, user_id: int, **kwargs) -> Optional[User]:
    """Actualiza la información de un usuario"""
    if "password" in kwargs:
        kwargs["hashed_password"] = hash_password(kwargs.pop("password"))
    
    return user_repository.update_user(db, user_id, **kwargs)


def deactivate_user(db: Session, user_id: int) -> bool:
    """Desactiva un usuario"""
    return user_repository.delete_user(db, user_id)


def get_all_users(db: Session) -> List[User]:
    """Obtiene todos los usuarios"""
    return db.query(User).all()


def change_user_email(db: Session, username: str, new_email: str) -> Optional[User]:
    """Cambia el email de un usuario"""
    user = user_repository.get_user_by_username(db, username)
    if not user:
        return None
    
    return user_repository.update_user(db, user.id, email=new_email)


def update_user_password(db: Session, username: str, new_password: str) -> Optional[User]:
    """Actualiza la contraseña de un usuario"""
    user = user_repository.get_user_by_username(db, username)
    if not user:
        return None
    
    hashed_pwd = hash_password(new_password)
    return user_repository.update_user(db, user.id, hashed_password=hashed_pwd)


def toggle_user_active_status(db: Session, username: str) -> Optional[User]:
    """Cambia el estado activo de un usuario"""
    user = user_repository.get_user_by_username(db, username)
    if not user:
        return None
    
    return user_repository.update_user(db, user.id, is_active=not user.is_active)


def change_user_role(db: Session, username: str, new_role: str) -> Optional[User]:
    """Cambia el rol de un usuario"""
    user = user_repository.get_user_by_username(db, username)
    if not user:
        return None
    
    return user_repository.update_user(db, user.id, role=new_role)


def get_jefes_carrera(db: Session) -> List[User]:
    """Obtiene todos los usuarios con rol JEFE_CARRERA"""
    return db.query(User).filter(User.role == "JEFE_CARRERA").all()

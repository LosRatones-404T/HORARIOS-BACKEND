from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from app.models import models
from app.core.security import hash_password
from typing import Optional


def create_user(db: Session, username: str, email: str, password: str, role: str = "user") -> models.User:
    """Crea un nuevo usuario en la base de datos"""
    hashed_pwd = hash_password(password)
    
    new_user = models.User(
        username=username,
        email=email,
        hashed_password=hashed_pwd,
        role=role,
        is_active=True
    )
    
    try:
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return new_user
    except IntegrityError:
        db.rollback()
        raise ValueError("El usuario o email ya existe")


def get_user_by_username(db: Session, username: str) -> Optional[models.User]:
    """Obtiene un usuario por su nombre de usuario"""
    return db.query(models.User).filter(models.User.username == username).first()


def get_user_by_id(db: Session, user_id: int) -> Optional[models.User]:
    """Obtiene un usuario por su ID"""
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_user_by_email(db: Session, email: str) -> Optional[models.User]:
    """Obtiene un usuario por su email"""
    return db.query(models.User).filter(models.User.email == email).first()


def update_user(db: Session, user_id: int, **kwargs) -> Optional[models.User]:
    """Actualiza los datos de un usuario"""
    user = get_user_by_id(db, user_id)
    if not user:
        return None
    
    for key, value in kwargs.items():
        if hasattr(user, key):
            setattr(user, key, value)
    
    db.commit()
    db.refresh(user)
    return user


def delete_user(db: Session, username: str) -> Optional[models.User]:
    """Elimina un usuario por su nombre de usuario"""
    user = get_user_by_username(db, username)
    if user:
        db.delete(user)
        db.commit()
        return user
    


# ELIMINAR O COMENTAR ESTA FUNCIÓN - Ya no existe Degree
# def get_degree_managed_by_user(db: Session, user_id: int) -> models.Degree | None:
#     """Obtiene la carrera gestionada por un usuario coordinador"""
#     return db.query(models.Degree).filter(models.Degree.coordinator_id == user_id).first()
from sqlalchemy.orm import Session
from app.models import models
from typing import Optional


def get_all_degrees(db: Session) -> list[models.Degree]:
    """Obtener todas las carreras"""
    return db.query(models.Degree).all()


def get_active_degrees(db: Session) -> list[models.Degree]:
    """Obtener carreras activas"""
    return db.query(models.Degree).filter(models.Degree.is_active.is_(True)).all()


def get_degree_by_id(db: Session, degree_id: str) -> Optional[models.Degree]:
    """Obtener una carrera por ID"""
    return db.query(models.Degree).filter(models.Degree.id == degree_id).first()


def get_degree_by_name(db: Session, name: str) -> Optional[models.Degree]:
    """Obtener una carrera por nombre"""
    return db.query(models.Degree).filter(models.Degree.name == name).first()


def create_degree(db: Session, id: str, name: str, jefe_carrera: Optional[str] = None, jefe_carrera_user_id: Optional[int] = None, is_active: bool = True) -> models.Degree:
    """Crear una nueva carrera"""
    degree = models.Degree(id=id, name=name, jefe_carrera=jefe_carrera, jefe_carrera_user_id=jefe_carrera_user_id, is_active=is_active)
    db.add(degree)
    db.commit()
    db.refresh(degree)
    return degree


def update_degree_jefe_carrera(db: Session, degree_id: str, jefe_carrera: str) -> Optional[models.Degree]:
    """Actualizar el jefe de carrera en turno"""
    degree = get_degree_by_id(db, degree_id)
    if degree:
        degree.jefe_carrera = jefe_carrera
        db.commit()
        db.refresh(degree)
        return degree
    return None


def update_degree(db: Session, degree_id: str, name: Optional[str] = None, 
                  jefe_carrera: Optional[str] = None, jefe_carrera_user_id: Optional[int] = None, 
                  is_active: Optional[bool] = None) -> Optional[models.Degree]:
    """Actualizar una carrera completa"""
    degree = get_degree_by_id(db, degree_id)
    if degree:
        if name is not None:
            degree.name = name
        if jefe_carrera is not None:
            degree.jefe_carrera = jefe_carrera
        if jefe_carrera_user_id is not None:
            degree.jefe_carrera_user_id = jefe_carrera_user_id
        if is_active is not None:
            degree.is_active = is_active
        db.commit()
        db.refresh(degree)
        return degree
    return None


def assign_jefe_carrera_user(db: Session, degree_id: str, user_id: int) -> Optional[models.Degree]:
    """Asignar un usuario del sistema como jefe de carrera"""
    degree = get_degree_by_id(db, degree_id)
    if degree:
        degree.jefe_carrera_user_id = user_id
        db.commit()
        db.refresh(degree)
        return degree
    return None


def toggle_degree_status(db: Session, degree_id: str) -> Optional[models.Degree]:
    """Cambiar el estado activo/inactivo de una carrera"""
    degree = get_degree_by_id(db, degree_id)
    if degree:
        degree.is_active = not degree.is_active
        db.commit()
        db.refresh(degree)
        return degree
    return None


def delete_degree(db: Session, degree_id: str) -> bool:
    """Eliminar una carrera"""
    degree = get_degree_by_id(db, degree_id)
    if degree:
        db.delete(degree)
        db.commit()
        return True
    return False

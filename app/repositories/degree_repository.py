from sqlalchemy.orm import Session
from app.models import unsis
from typing import List, Optional


def get_all_carreras(db: Session) -> List[unsis.Carrera]:
    """Obtiene todas las carreras activas"""
    return db.query(unsis.Carrera).filter(unsis.Carrera.vigente == True).all()


def get_carrera_by_clave(db: Session, clave: str) -> Optional[unsis.Carrera]:
    """Obtiene una carrera por su clave"""
    return db.query(unsis.Carrera).filter(unsis.Carrera.clave == clave).first()


def get_carreras_con_grupos(db: Session) -> List[unsis.Carrera]:
    """Obtiene carreras que tienen grupos activos"""
    return db.query(unsis.Carrera).join(unsis.Grupo).distinct().all()

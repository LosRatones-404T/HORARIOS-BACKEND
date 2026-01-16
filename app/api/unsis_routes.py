from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.core.conexion import get_db
from app.models import models

from app.schemas.examen_schemas import ExamResponse, MessageResponse

router = APIRouter(
    prefix="/unsis",
    tags=["unsis"]
)

# obtener periodo aun en proceso de correción
@router.get("/current-period", response_model=MessageResponse)
def get_current_exam_period(db: Session = Depends(get_db)):
    """
    Retorna el periodo actual de exámenes.
    """
    from app.repositories.examen_repositories import get_current_exam_period

    current_period = get_current_exam_period(db)

    if not current_period:
        raise HTTPException(status_code=404, detail="No se encontró un periodo de exámenes activo.")

    return {"message": f"El periodo actual de exámenes es: {current_period}."}

# obtener carreraas activas
@router.get("/degrees", response_model=List[MessageResponse])
def get_active_degrees(db: Session = Depends(get_db)):
    """
    Retorna la lista de carreras activas.
    """
    from app.repositories.examen_repositories import get_all_degrees

    degrees = get_all_degrees(db)

    if not degrees:
        raise HTTPException(status_code=404, detail="No se encontraron carreras activas.")

    results = []
    for degree in degrees:
        results.append({"message": f"Carrera: {degree.name}, Jefe: {degree.jefe_carrera}"})

    return results

# obtener aulas 
@router.get("/classrooms", response_model=List[MessageResponse])
def get_all_classrooms(db: Session = Depends(get_db)):
    """
    Retorna la lista de aulas disponibles.
    """
    from app.repositories.examen_repositories import get_all_classrooms

    classrooms = get_all_classrooms(db)

    if not classrooms:
        raise HTTPException(status_code=404, detail="No se encontraron aulas disponibles.")

    results = []
    for classroom in classrooms:
        results.append({"message": f"Aula: {classroom.nombre}, Capacidad: {classroom.capacidad}, Tipo: {classroom.tipo}"})

    return results
####################GRUPOS#########################
# obtener todos los grupos
@router.get("/groups", response_model=List[MessageResponse])
def get_all_groups(db: Session = Depends(get_db)):
    """
    Retorna la lista de grupos.
    """
    from app.models import unsis

    groups = db.query(unsis.Grupo).all()

    if not groups:
        raise HTTPException(status_code=404, detail="No se encontraron grupos.")

    results = []
    for group in groups:
        results.append({"message": f"Grupo: {group.nombre}, Carrera ID: {group.carrera_id}, Periodo ID: {group.periodo_id}"})

    return results

# Obtenr grupos por carrera
@router.get("/groups-by-degree/{degree_id}", response_model=List[MessageResponse])
def get_groups_by_degree(degree_id: str, db: Session = Depends(get_db)):
    """
    Retorna la lista de grupos para una carrera específica.
    """
    from app.repositories.examen_repositories import get_grupos_by_degree

    groups = get_grupos_by_degree(db, degree_id)

    if not groups:
        raise HTTPException(status_code=404, detail="No se encontraron grupos para la carrera especificada.")

    results = []
    for group in groups:
        results.append({"message": f"Grupo: {group.nombre}, Carrera ID: {group.carrera_id}, Periodo ID: {group.periodo_id}"})

    return results

# obtener grupos por carrera y semestre
@router.get("/groups-by-degree-and-semester/{degree_id}/{semester}", response_model=List[MessageResponse])
def get_groups_by_degree_and_semester(degree_id: str, semester: int, db: Session = Depends(get_db)):
    """
    Retorna la lista de grupos para una carrera y semestre específicos.
    """
    from app.repositories.examen_repositories import get_grupos_by_degree_and_semester

    groups = get_grupos_by_degree_and_semester(db, degree_id, semester)

    if not groups:
        raise HTTPException(status_code=404, detail="No se encontraron grupos para la carrera y semestre especificados.")

    results = []
    for group in groups:
        results.append({"message": f"Grupo: {group.nombre}, Carrera ID: {group.carrera_id}, Periodo ID: {group.periodo_id}, Semestre: {group.semestre}"})

    return results

# obtener periodo actual de unsis
@router.get("/current-unsis-period", response_model=MessageResponse)
def get_current_unsis_period(db: Session = Depends(get_db)):
    """
    Retorna el periodo actual de Unsis.
    """
    from app.repositories.examen_repositories import get_current_unsis_period

    current_period = get_current_unsis_period(db)

    if not current_period:
        raise HTTPException(status_code=404, detail="No se encontró un periodo actual en Unsis.")

    return {"message": f"El periodo actual de Unsis es: {current_period}."}
# from app.schemas.unsis_schemas import GrupoResponse, AulaResponse, CarreraResponse, PeriodoExamenResponse, MateriaResponse, HorarioResponse, PeriodoResponse, ProfesorResponse, MateriaResponse
from app.schemas import unsis_schemas
from app.services import unsis_service
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.core.conexion import get_db
from app.models import models

from app.schemas.examen_schemas import ExamResponse, MessageResponse
from app.repositories import unsis_repository
from app.repositories import examen_repositories
from app.models import unsis

router = APIRouter(
    prefix="/unsis",
    tags=["unsis"]
)

# obtener periodo actual de unsis (semestre actual)
@router.get("/current-period", response_model=unsis_schemas.PeriodoResponse)
def get_current_exam_period(db: Session = Depends(get_db)):
    """
    Retorna el periodo actual de exámenes en formato JSON estándar.
    """
    current_period = unsis_repository.get_current_unsis_period(db)

    if not current_period:
        raise HTTPException(status_code=404, detail="No se encontró un periodo de exámenes activo.")

    return current_period

# actualizar datos de periodo actual de unsis
@router.post("/update-current-period", response_model=unsis_schemas.PeriodoResponse)
def update_current_unsis_period(period: unsis_schemas.PeriodoResponse, db: Session = Depends(get_db)):
    """
    Insertar o actualizar las fechas de parciales del periodo actual.
    """
    return unsis_service.update_current_period(db, period)

# obtener carreras activas
@router.get("/degrees", response_model=List[unsis_schemas.CarreraResponse])
def get_active_degrees(db: Session = Depends(get_db)):
    """
    Retorna la lista de carreras activas en formato JSON estándar.
    """
    degrees = unsis_repository.get_active_degrees(db)

    if not degrees:
        raise HTTPException(status_code=404, detail="No se encontraron carreras activas.")

    return degrees

# obtener aulas 
@router.get("/classrooms", response_model=List[unsis_schemas.AulaResponse])
def get_all_classrooms(db: Session = Depends(get_db)):
    """
    Retorna la lista de aulas disponibles en formato JSON estándar.
    """
    classrooms = unsis_repository.get_all_classrooms(db)

    if not classrooms:
        raise HTTPException(status_code=404, detail="No se encontraron aulas disponibles.")

    return classrooms
####################GRUPOS#########################
# obtener todos los grupos
@router.get("/groups", response_model=List[unsis_schemas.GrupoResponse])
def get_all_groups(db: Session = Depends(get_db)):
    """
    Retorna la lista de grupos en formato JSON estándar.
    """
    groups = unsis_repository.get_all_groups(db)

    if not groups:
        raise HTTPException(status_code=404, detail="No se encontraron grupos.")

    return groups

# Obtenr grupos por carrera
@router.get("/groups-by-degree/{degree_id}", response_model=List[unsis_schemas.GrupoResponse])
def get_groups_by_degree(degree_id: str, db: Session = Depends(get_db)):
    """
    Retorna la lista de grupos para una carrera específica en formato JSON estándar.
    """
    groups = unsis_repository.get_grupos_by_degree(db, degree_id)

    if not groups:
        raise HTTPException(status_code=404, detail="No se encontraron grupos para la carrera especificada.")

    return groups

# obtener grupos por carrera y semestre
@router.get("/groups-by-degree-and-semester/{degree_id}/{semester}", response_model=List[unsis_schemas.GrupoResponse])
def get_groups_by_degree_and_semester(degree_id: str, semester: int, db: Session = Depends(get_db)):
    """
    Retorna la lista de grupos para una carrera y semestre específicos en formato JSON estándar.
    """
    groups = unsis_repository.get_grupos_by_degree_and_semester(db, degree_id, semester)

    if not groups:
        raise HTTPException(status_code=404, detail="No se encontraron grupos para la carrera y semestre especificados.")

    return groups

# obtener grupos por materia
@router.get("/groups-by-subject/{subject_id}", response_model=List[unsis_schemas.GrupoResponse])
def get_groups_by_subject(subject_id: str, db: Session = Depends(get_db)):
    """
    Retorna la lista de grupos que cursan una materia específica en formato JSON estándar.
    """
    groups = unsis_repository.get_groups_by_subject(db, subject_id)

    if not groups:
        raise HTTPException(status_code=404, detail="No se encontraron grupos para la materia especificada.")

    return groups

####################MATERIAS#########################
# obtener todas las materias
@router.get("/subjects", response_model=List[unsis_schemas.MateriaResponse])
def get_all_subjects(db: Session = Depends(get_db)):
    """
    Retorna la lista de materias en formato JSON estándar.
    """
    subjects = unsis_repository.get_all_subjects(db)

    if not subjects:
        raise HTTPException(status_code=404, detail="No se encontraron materias.")

    return subjects

# obtener materias por carrera
@router.get("/subjects-by-degree/{degree_id}", response_model=List[unsis_schemas.MateriaResponse])
def get_subjects_by_degree(degree_id: str, db: Session = Depends(get_db)):
    """
    Retorna la lista de materias para una carrera específica en formato JSON estándar.
    """
    subjects = unsis_repository.get_subjects_by_degree(db, degree_id)

    if not subjects:
        raise HTTPException(status_code=404, detail="No se encontraron materias para la carrera especificada.")

    return subjects

# obtener materias por carrera y semestre
@router.get("/subjects-by-degree-and-semester/{degree_id}/{semester}", response_model=List[unsis_schemas.MateriaResponse])
def get_subjects_by_degree_and_semester(degree_id: str, semester: int, db: Session = Depends(get_db)):
    """
    Retorna la lista de materias para una carrera y semestre específicos en formato JSON estándar.
    """
    subjects = unsis_repository.get_subjects_by_degree_and_semester(db, degree_id, semester)

    if not subjects:
        raise HTTPException(status_code=404, detail="No se encontraron materias para la carrera y semestre especificados.")

    return subjects

####################HORARIOS#########################
# obtener todos los horarios
@router.get("/schedules", response_model=List[unsis_schemas.HorarioResponse])
def get_all_schedules(db: Session = Depends(get_db)):
    """
    Retorna la lista de horarios en formato JSON estándar.
    """
    schedules = unsis_repository.get_all_schedules(db)

    if not schedules:
        raise HTTPException(status_code=404, detail="No se encontraron horarios.")

    return schedules

# obtener horarios por grupo
@router.get("/schedules-by-group/{group_id}", response_model=List[unsis_schemas.HorarioResponse])
def get_schedules_by_group(group_id: str, db: Session = Depends(get_db)):
    """
    Retorna la lista de horarios para un grupo específico en formato JSON estándar.
    """
    schedules = unsis_repository.get_schedules_by_group(db, group_id)

    if not schedules:
        raise HTTPException(status_code=404, detail="No se encontraron horarios para el grupo especificado.")

    return schedules

####################PROFESORES#########################
# obtener todos los profesores
@router.get("/professors", response_model=List[unsis_schemas.ProfesorResponse])
def get_all_professors(db: Session = Depends(get_db)):
    """
    Retorna la lista de profesores en formato JSON estándar.
    """
    professors = unsis_repository.get_all_professors(db)

    if not professors:
        raise HTTPException(status_code=404, detail="No se encontraron profesores.")

    return professors

# obtener profesores por materia
@router.get("/professors-by-subject/{subject_id}", response_model=List[unsis_schemas.ProfesorResponse])
def get_professors_by_subject(subject_id: str, db: Session = Depends(get_db)):
    """
    Retorna la lista de profesores que imparten una materia específica en formato JSON estándar.
    """
    professors = unsis_repository.get_professors_by_subject(db, subject_id)

    if not professors:
        raise HTTPException(status_code=404, detail="No se encontraron profesores para la materia especificada.")

    return professors



from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.core.conexion import get_db
from app.models import models

from app.schemas.examen_schemas import ExamResponse, MessageResponse, ExamSpecCreate, ExamSpecResponse
from app.services.examen_service import generate_exam_schedule_degree

router = APIRouter(
    prefix="/examenes", 
    tags=["examenes"])

@router.get("/exams", response_model=List[ExamResponse])
def get_all_exams(db: Session = Depends(get_db)):
    """
    Retorna la lista de exámenes agendados.
    """
    exams = db.query(models.Exam).all()
    
    # Mapeamos los objetos de DB al formato JSON plano que definimos en el Schema
    results = []
    for exam in exams:
        results.append({
            "id": exam.id,
            "course": exam.course.name,
            "group": exam.course.group_name,
            "professor": exam.course.professor.full_name,
            "classroom": exam.classroom.name,
            "date": exam.exam_date,
            "start": exam.start_time,
            "end": exam.end_time
        })
    
    return results

# obtener examenes por periodo
@router.get("/exams-by-period/{period}", response_model=List[ExamResponse])
def get_exams_by_period(period: str, db: Session = Depends(get_db)):
    """
    Retorna la lista de exámenes agendados para un periodo específico.
    """

    exams = get_exams_by_period(db, period)
    
    # Mapeamos los objetos de DB al formato JSON plano que definimos en el Schema
    results = []
    for exam in exams:
        results.append({
            "id": exam.id,
            "course": exam.course.name,
            "group": exam.course.group_name,
            "professor": exam.course.professor.full_name,
            "classroom": exam.classroom.name,
            "date": exam.exam_date,
            "start": exam.start_time,
            "end": exam.end_time
        })
    
    return results

# generar examenes para una carrera
@router.post("/generate-schedule/{degree_id}", response_model=MessageResponse)
def generate_exam_schedule(degree_id: str, db: Session = Depends(get_db)):
    """
    Genera el calendario de exámenes para una carrera específica.
    """

    exams_created = generate_exam_schedule_degree(db, degree_id)

    if not exams_created:
        raise HTTPException(status_code=400, detail="No se pudieron generar exámenes para la carrera especificada.")

    return {"message": f"Se generaron {len(exams_created)} exámenes para la carrera con ID {degree_id}."}


# # set or update exam preferences for a course
# @router.post("/set-exam-preferences/{course_id}", response_model=MessageResponse)
# def set_exam_preferences(course_id: str, preferences: dict, db: Session = Depends(get_db)):
#     """
#     Define o actualiza las preferencias de examen para un curso específico.
#     """

#     models.definir_preferencias_examen(course_id, preferences)

#     return {"message": f"Preferencias de examen actualizadas para el curso con ID {course_id}."}


# Crear o actualizar especificaciones de examen
@router.post("/exam-specifications", response_model=ExamSpecResponse, status_code=201)
def create_exam_specification(exam_spec: ExamSpecCreate, db: Session = Depends(get_db)):
    """
    Crea o actualiza las especificaciones de examen para un curso.
    Si ya existe una especificación para el curso, se actualiza.
    """
    from app.repositories.examen_repositories import save_or_update_exam_specifications
    
    # Crear el modelo de SQLAlchemy desde el schema Pydantic
    db_exam_spec = models.ExamSpecifications(**exam_spec.model_dump())
    
    # Guardar o actualizar
    saved_spec = save_or_update_exam_specifications(db, db_exam_spec)
    
    return saved_spec


# # Obtener especificaciones de examen por curso
# @router.get("/exam-specifications/{course_id}", response_model=ExamSpecResponse)
# def get_exam_specification(course_id: int, db: Session = Depends(get_db)):
#     """
#     Obtiene las especificaciones de examen para un curso específico.
#     """
#     from app.repositories.examen_repositories import get_exam_especifications_by_course
    
#     spec = get_exam_especifications_by_course(db, course_id)
    
#     if not spec:
#         raise HTTPException(status_code=404, detail="No se encontraron especificaciones para este curso")
    
#     return spec
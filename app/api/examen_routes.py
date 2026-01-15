from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.core.conexion import get_db
from app.models import models

from app.schemas.examen_schemas import ExamResponse, MessageResponse

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
    from app.repositories.examen_repositories import get_exams_by_period

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
def generate_exam_schedule(degree_id: int, db: Session = Depends(get_db)):
    """
    Genera el calendario de exámenes para una carrera específica.
    """
    from app.services.examen_service import generate_exam_schedule_degree

    exams_created = generate_exam_schedule_degree(db, degree_id)

    if not exams_created:
        raise HTTPException(status_code=400, detail="No se pudieron generar exámenes para la carrera especificada.")

    return {"message": f"Se generaron {len(exams_created)} exámenes para la carrera con ID {degree_id}."}



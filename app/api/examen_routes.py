from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import date, time, timedelta
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

@router.post("/seed-pdf-data", response_model=MessageResponse)
def seed_data_from_pdf(db: Session = Depends(get_db)):
    """
    Endpoint temporal para cargar datos reales del PDF (Informática 106-A)
    """
    # 1. Verificar si ya existen datos para no duplicar
    if db.query(models.Course).filter(models.Course.group_name == "106-A").first():
        return {"message": "Los datos ya fueron cargados previamente."}

    # 2. Crear Profesores (Datos del PDF)
    prof_irving = models.Professor(full_name="Mtro. Irving Ulises Hernández Miguel")
    prof_fabiola = models.Professor(full_name="M.I.S. Fabiola Crespo Barrios")
    prof_oswaldo = models.Professor(full_name="M.I.T.I. Oswaldo Rey Ávila Barrón")
    
    db.add_all([prof_irving, prof_fabiola, prof_oswaldo])
    db.commit()

    # 3. Crear Aulas
    classroom_ceti = models.Classroom(name="CETI-S.O.", capacity=30, is_computer_lab=True)
    classroom_e2 = models.Classroom(name="E2", capacity=40)
    classroom_d4 = models.Classroom(name="D4", capacity=40)
    
    db.add_all([classroom_ceti, classroom_e2, classroom_d4])
    db.commit()

    # 4. Crear Materias y asignar Exámenes
    # Datos extraídos de: LICENCIATURA EN INFORMÁTICA.pdf (Página 2)
    
    # Materia 1: Diseño Estructurado
    course1 = models.Course(name="Diseño Estructurado de Algoritmos", group_name="106-A", professor_id=prof_irving.id)
    db.add(course1)
    db.commit()
    
    exam1 = models.Exam(
        course_id=course1.id,
        classroom_id=classroom_ceti.id,
        exam_date=date(2025, 10, 28), # 28/10/2025
        start_time=time(17, 0),       # 17:00
        end_time=time(19, 0)          # Asumimos 2 horas
    )

    # Materia 2: Administración
    course2 = models.Course(name="Administración", group_name="106-A", professor_id=prof_fabiola.id)
    db.add(course2)
    db.commit()

    exam2 = models.Exam(
        course_id=course2.id,
        classroom_id=classroom_e2.id,
        exam_date=date(2025, 10, 29), # 29/10/2025
        start_time=time(13, 0),       # 13:00
        end_time=time(15, 0)
    )

    # Materia 3: Historia del Pensamiento Filosófico
    course3 = models.Course(name="Historia del Pensamiento Filosófico", group_name="106-A", professor_id=prof_oswaldo.id)
    db.add(course3)
    db.commit()

    exam3 = models.Exam(
        course_id=course3.id,
        classroom_id=classroom_d4.id,
        exam_date=date(2025, 10, 30), # 30/10/2025
        start_time=time(16, 0),       # 16:00
        end_time=time(18, 0)
    )

    db.add_all([exam1, exam2, exam3])
    db.commit()

    return {"message": "Datos del PDF (Grupo 106-A) cargados exitosamente"}
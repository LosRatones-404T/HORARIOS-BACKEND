from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.core.conexion import get_db
from app.models import models, unsis

from app.schemas.examen_schemas import ExamResponse, MessageResponse, ExamSpecCreate, ExamSpecResponse
from app.services import examen_service
from app.repositories import examen_repositories

router = APIRouter(
    prefix="/examenes", 
    tags=["examenes"])

@router.get("/exams", response_model=List[ExamResponse])
def get_all_exams(db: Session = Depends(get_db)):
    """Retorna todos los exámenes agendados"""
    exams = db.query(models.Exam).all()
    
    results = []
    for exam in exams:
        # Obtener datos de UNSIS
        materia = db.query(unsis.Materia).filter(unsis.Materia.id == exam.materia_id).first()
        aula = db.query(unsis.Aula).filter(unsis.Aula.clave == exam.aula_id).first()
        profesor = db.query(unsis.Profesor).filter(unsis.Profesor.id == exam.profesor_id).first()
        
        results.append({
            "id": exam.id,
            "course": materia.nombre if materia else "Sin materia",
            "group": exam.grupo_id or "Todos",
            "professor": profesor.nombre if profesor else "Sin asignar",
            "classroom": aula.nombre if aula else "Sin asignar",
            "date": exam.exam_date,
            "start": exam.start_time,
            "end": exam.end_time
        })
    
    return results

@router.get("/exams-by-period/{period}", response_model=List[ExamResponse])
def get_exams_by_period_route(period: str, db: Session = Depends(get_db)):
    """Retorna exámenes de un periodo específico"""
    exams = examen_repositories.get_exams_period(db, period)
    
    results = []
    for exam in exams:
        materia = db.query(unsis.Materia).filter(unsis.Materia.id == exam.materia_id).first()
        aula = db.query(unsis.Aula).filter(unsis.Aula.id == exam.aula_id).first()
        profesor = db.query(unsis.Profesor).filter(unsis.Profesor.id == exam.profesor_id).first()
        
        results.append({
            "id": exam.id,
            "course": materia.nombre if materia else "Sin materia",
            "group": exam.grupo_id or "Todos",
            "professor": profesor.nombre if profesor else "Sin asignar",
            "classroom": aula.nombre if aula else "Sin asignar",
            "date": exam.exam_date,
            "start": exam.start_time,
            "end": exam.end_time
        })
    
    return results

@router.post("/generate-schedule/{degree_id}", response_model=MessageResponse)
def generate_exam_schedule(degree_id: str, db: Session = Depends(get_db)):
    """Genera exámenes del primer parcial para una carrera"""
    resultado = examen_service.generate_exam_schedule_degree(db, degree_id, "PRIMER_PARCIAL")

    if not resultado.get("success"):
        raise HTTPException(
            status_code=400, 
            detail=resultado.get("error", "Error generando exámenes")
        )

    return {
        "message": f"Creados: {resultado['examenes_creados']}, Conflictos: {resultado['examenes_conflicto']}"
    }

@router.post("/exam-specifications", response_model=ExamSpecResponse, status_code=201)
def create_exam_specification(exam_spec: ExamSpecCreate, db: Session = Depends(get_db)):
    """Crear o actualizar especificaciones de examen"""
    db_exam_spec = models.ExamSpecification(**exam_spec.model_dump())
    saved_spec = examen_repositories.save_or_update_exam_specifications(db, db_exam_spec)
    return saved_spec

@router.post("/generate/{degree_id}/{tipo_examen}")
def generate_exams_for_degree_and_type(
    degree_id: str,
    tipo_examen: str,
    db: Session = Depends(get_db)
):
    """Generar exámenes para una carrera y tipo específico"""
    resultado = examen_service.generate_exam_schedule_degree(db, degree_id, tipo_examen)
    return resultado

@router.post("/generate-all/{degree_id}")
def generate_all_exams_for_degree(
    degree_id: str,
    db: Session = Depends(get_db)
):
    """Generar todos los periodos de examen para una carrera"""
    resultados = examen_service.generar_todos_los_examenes_carrera(db, degree_id)
    return resultados

@router.get("/materias-by-carrera/{degree_id}")
def get_materias_by_carrera(degree_id: str, db: Session = Depends(get_db)):
    """Obtener materias de una carrera"""
    materias = db.query(unsis.Materia).join(
        unsis.Horario, unsis.Horario.materia_id == unsis.Materia.id
    ).join(
        unsis.Grupo, unsis.Grupo.clave == unsis.Horario.grupo_id
    ).filter(
        unsis.Grupo.carrera_id == degree_id
    ).distinct().all()
    
    return [{"id": m.id, "nombre": m.nombre} for m in materias]

# eliminar todos los examenes (para pruebas)
@router.delete("/delete-all", response_model=MessageResponse)
def delete_all_exams_route(db: Session = Depends(get_db)):
    """Eliminar todos los exámenes (solo para pruebas)"""
    examen_repositories.delete_all_exams(db)
    return {"message": "Todos los exámenes han sido eliminados."}
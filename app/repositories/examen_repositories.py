from app.models import unsis
import app.models.models as models
from app.repositories.unsis_repository import get_current_unsis_period
from app.schemas.examen_schemas import ExamSpecCreate
from sqlalchemy.orm import Session





# obtener examenes generados por periodo
def get_exams_by_period(db: Session, period: str):
    # Buscar exámenes que tengan especificaciones con el periodo especificado
    return db.query(models.Exam).join(
        models.ExamSpecifications, 
        models.Exam.course_id == models.ExamSpecifications.id
    ).filter(
        models.ExamSpecifications.periodo_actual == period
    ).all()

# obtener examenes generados por periodo y curso
def get_exams_by_period_and_course(db: Session, period: str, course_id: int):
    return db.query(models.Exam).join(
        models.ExamSpecifications, 
        models.Exam.course_id == models.ExamSpecifications.id
    ).filter(
        models.ExamSpecifications.periodo_actual == period,
        models.Exam.course_id == course_id
    ).all()

# obtener examenes generados en el periodo de examenes actual
def get_exams_period(db: Session, period: str, exam_type: str):
    return db.query(models.Exam).join(
        models.ExamSpecifications, 
        models.Exam.course_id == models.ExamSpecifications.id
    ).filter(
        models.ExamSpecifications.periodo_actual == period,
        models.Exam.examen_type == exam_type
    ).all()

# obtener especificaciones de examen por curso
def get_exam_especifications_by_course(db: Session, course_id: int):
    return db.query(models.ExamSpecifications).filter(
        models.ExamSpecifications.course_id == course_id
    ).first()


# guardar examen
def save_exam(db: Session, exam: models.Exam):
    db.add(exam)
    db.commit()
    db.refresh(exam)
    return exam

# guardar o actualizar especificaciones de examen
def save_or_update_exam_specifications(db: Session, exam_spec: models.ExamSpecification):  # ❌ era ExamSpecifications
    existing_spec = db.query(models.ExamSpecification).filter(
        models.ExamSpecification.course_id == exam_spec.course_id,
        models.ExamSpecification.tipo_examen == exam_spec.tipo_examen
    ).first()
    
    if existing_spec:
        # Actualizar
        existing_spec.tipo_aplicacion = exam_spec.tipo_aplicacion
        existing_spec.es_academia = exam_spec.es_academia
        existing_spec.profesor_aplicador_id = exam_spec.profesor_aplicador_id
        existing_spec.duracion_minutos = exam_spec.duracion_minutos
        existing_spec.preferencia_aula_id = exam_spec.preferencia_aula_id
        existing_spec.notas = exam_spec.notas
        db.commit()
        db.refresh(existing_spec)
        return existing_spec
    else:
        # Crear nuevo
        db.add(exam_spec)
        db.commit()
        db.refresh(exam_spec)
        return exam_spec

def get_exam_especifications_by_course(db: Session, course_id: str):
    return db.query(models.ExamSpecification).filter(
        models.ExamSpecification.course_id == course_id
    ).all() 



def create_exam_spec(self, exam_data: ExamSpecCreate):
        # Convertimos el esquema Pydantic a Modelo SQLAlchemy
        # **exam_data.dict() desempaqueta los campos automáticamente
        db_exam = models.ExamSpecification(**exam_data.dict())
        
        self.db.add(db_exam)
        self.db.commit()
        self.db.refresh(db_exam) # Obtiene el ID generado por la BD
        return db_exam

def get_by_materia(self, materia_id: str):
    return self.db.query(models.ExamSpecifications).filter(models.ExamSpecifications.materia_id == materia_id).all()

# obtener periodo actual de examenes, primer parcial, segundo parcial, ordinario
def get_current_exam_period(db: Session):
    # Obtener el periodo de exámenes más reciente
    current_period = db.query(models.PeriodosExamenes).order_by(models.PeriodosExamenes.id.desc()).first()
    if current_period:
        return current_period.nombre_periodo
    return None

################################## Propuesta

from datetime import datetime, time, date, timedelta
from typing import List, Tuple, Optional

def get_grupos_by_course(db: Session, course_id: str):
    """Obtener todos los grupos asociados a un curso"""
    return db.query(unsis.Grupo).join(
        unsis.Horario, unsis.Horario.grupo_id == unsis.Grupo.clave
    ).filter(
        unsis.Horario.materia_id == course_id
    ).distinct().all()

def get_courses_academia_by_subject(db: Session, course_id: str):
    """Obtener todos los cursos que pertenecen a la misma materia (academia)"""
    curso = db.query(unsis.Horario).filter(unsis.Horario.materia_id == course_id).first()
    if not curso:
        return []
    
    return db.query(unsis.Horario).filter(
        unsis.Horario.materia_id == curso.materia_id
    ).distinct().all()

def get_exams_by_date_and_time(db: Session, exam_date: date, start_time: time, end_time: time):
    """Obtener exámenes en una fecha y rango de tiempo específico"""
    return db.query(models.Exam).filter(
        models.Exam.exam_date == exam_date,
        models.Exam.start_time < end_time,
        models.Exam.end_time > start_time
    ).all()

def get_exams_by_classroom_and_datetime(db: Session, classroom_id: str, exam_date: date, start_time: time, end_time: time):
    """Obtener exámenes en un aula, fecha y hora específicas"""
    return db.query(models.Exam).filter(
        models.Exam.classroom_id == classroom_id,
        models.Exam.exam_date == exam_date,
        models.Exam.start_time < end_time,
        models.Exam.end_time > start_time
    ).all()

def get_exams_by_professor_and_datetime(db: Session, professor_id: str, exam_date: date, start_time: time, end_time: time):
    """Obtener exámenes donde un profesor aplica en una fecha y hora específicas"""
    return db.query(models.Exam).filter(
        models.Exam.professor_id == professor_id,
        models.Exam.exam_date == exam_date,
        models.Exam.start_time < end_time,
        models.Exam.end_time > start_time
    ).all()

def get_classrooms_by_type(db: Session, tipo: str):
    """Obtener aulas por tipo (computadora o normales)"""
    if tipo == "COMPUTADORA":
        return db.query(unsis.Aula).filter(unsis.Aula.tipo == "COMPUTADORA").all()
    else:
        return db.query(unsis.Aula).filter(
            (unsis.Aula.tipo == "AULA") | (unsis.Aula.tipo.is_(None))
        ).all()

def get_exam_periods_dates(db: Session):
    """Obtener las fechas de todos los periodos de examen del periodo actual"""
    current_period = get_current_unsis_period(db)
    if not current_period:
        return None
    
    return {
        "PRIMER_PARCIAL": (current_period.primer_parcial_inicio, current_period.primer_parcial_fin),
        "SEGUNDO_PARCIAL": (current_period.segundo_parcial_inicio, current_period.segundo_parcial_fin),
        "TERCER_PARCIAL": (current_period.tercer_parcial_inicio, current_period.tercer_parcial_fin),
        "ORDINARIO": (current_period.ordinario_inicio, current_period.ordinario_fin),
        "EXTRA_1": (current_period.extra1_inicio, current_period.extra1_fin),
        "EXTRA_2": (current_period.extra2_inicio, current_period.extra2_fin),
        "ESPECIAL": (current_period.especial_inicio, current_period.especial_fin),
    }

#######################

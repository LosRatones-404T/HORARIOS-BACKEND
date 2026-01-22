from app.models import unsis
import app.models.models as models
from app.schemas.examen_schemas import ExamSpecCreate
from sqlalchemy.orm import Session

# otener cursos por carrera
def get_courses_by_degree(db: Session, degree_id: str):
    # TODO: devolver materias activas por carrera 
    # return db.query(models.Course).filter(models.Course.degree_id == degree_id).all()
    return []

# obtener aulas
def get_all_classrooms(db: Session):
    return db.query(unsis.Aula).all()

# obtener grupos por carrera
def get_grupos_by_degree(db: Session, degree_id: str):
    return db.query(unsis.Grupo).filter(unsis.Grupo.carrera_id == degree_id).all()

# obtener grupos por carrera y semestre
def get_grupos_by_degree_and_semester(db: Session, degree_id: str, semester: int):
    return db.query(unsis.Grupo).filter(
        unsis.Grupo.carrera_id == degree_id,
        unsis.Grupo.semestre == semester
    ).all()

# obtener grupos por materia
def get_groups_by_subject(db: Session, subject_id: str):
    return db.query(unsis.Grupo).join(
        unsis.Horario, unsis.Horario.grupo_id == unsis.Grupo.clave
    ).filter(
        unsis.Horario.materia_id == subject_id
    ).distinct().all()

# obtener periodo actual de unsis
def get_current_unsis_period(db: Session):
    current_period = db.query(unsis.Periodo).order_by(unsis.Periodo.id.desc()).first()
    if current_period:
        return current_period.clave
    return None

# obtener periodo actual de examenes
def get_current_exam_period(db: Session):
    # Obtener el periodo de exámenes más reciente
    current_period = db.query(models.PeriodosExamenes).order_by(models.PeriodosExamenes.id.desc()).first()
    if current_period:
        return current_period.nombre_periodo
    return None

# obtener todas las carreras
def get_all_degrees(db: Session):
    return db.query(unsis.Carrera).all()

# obtener carreras activas
def get_active_degrees(db: Session):
    return db.query(unsis.Carrera).filter(unsis.Carrera.vigente == True).all()

# obtener todos los grupos
def get_all_groups(db: Session):
    return db.query(unsis.Grupo).all()

# obtener todas las materias
def get_all_subjects(db: Session):
    return db.query(unsis.Materia).all()

# obtener materias por carrera
def get_subjects_by_degree(db: Session, degree_id: str):
    return db.query(unsis.Materia).join(
        unsis.Horario, unsis.Horario.materia_id == unsis.Materia.id
    ).join(
        unsis.Grupo, unsis.Grupo.clave == unsis.Horario.grupo_id
    ).filter(
        unsis.Grupo.carrera_id == degree_id
    ).distinct().all()

# obtener materias por carrera y semestre
def get_subjects_by_degree_and_semester(db: Session, degree_id: str, semester: int):
    return db.query(unsis.Materia).join(
        unsis.Horario, unsis.Horario.materia_id == unsis.Materia.id
    ).join(
        unsis.Grupo, unsis.Grupo.clave == unsis.Horario.grupo_id
    ).filter(
        unsis.Grupo.carrera_id == degree_id,
        unsis.Grupo.semestre == semester
    ).distinct().all()

# obtener todos los horarios
def get_all_schedules(db: Session):
    return db.query(unsis.Horario).all()

# obtener horarios por grupo
def get_schedules_by_group(db: Session, group_id: str):
    return db.query(unsis.Horario).filter(unsis.Horario.grupo_id == group_id).all()

# obtener todos los profesores
def get_all_professors(db: Session):
    return db.query(unsis.Profesor).all()

# obtener profesores por materia
def get_professors_by_subject(db: Session, subject_id: str):
    return db.query(unsis.Profesor).join(
        unsis.Horario, unsis.Horario.profesor_id == unsis.Profesor.id
    ).filter(
        unsis.Horario.materia_id == subject_id
    ).distinct().all()

# obtener periodo actual de examenes

# buscar una aula disponible en una fecha y hora específicas
def classroom_available(db: Session, exam_date, start_time, end_time, required_capacity: int = 0, is_computer_lab: bool = False):
    """
    Busca un aula disponible en una fecha y hora específicas.
    
    Args:
        db: Sesión de base de datos
        exam_date: Fecha del examen (date)
        start_time: Hora de inicio (time)
        end_time: Hora de fin (time)
        required_capacity: Capacidad mínima requerida (opcional)
        is_computer_lab: Si se requiere sala de cómputo (opcional)
        
    Returns:
        str: ID del aula disponible o None si no hay aulas disponibles
    """
    from datetime import datetime, time
    
    # Obtener todas las aulas que cumplen con los requisitos básicos
    query = db.query(unsis.Aula)
    
    if required_capacity > 0:
        query = query.filter(unsis.Aula.capacidad >= required_capacity)
    
    if is_computer_lab:
        query = query.filter(unsis.Aula.tipo.in_(["LABORATORIO", "SALA DE COMPUTO"]))
    
    available_classrooms = query.all()
    
    if not available_classrooms:
        return None
    
    # Verificar qué aulas no tienen exámenes en ese horario
    for classroom in available_classrooms:
        # Verificar si hay un examen programado en esa aula en esa fecha y hora
        conflicting_exam = db.query(models.Exam).join(
            models.Classroom, models.Exam.classroom_id == models.Classroom.id
        ).filter(
            models.Classroom.name == classroom.nombre,
            models.Exam.exam_date == exam_date,
            models.Exam.start_time < end_time,
            models.Exam.end_time > start_time
        ).first()
        
        if not conflicting_exam:
            # Esta aula está disponible
            return classroom.clave
    
    # No hay aulas disponibles en ese horario
    return None
    
    
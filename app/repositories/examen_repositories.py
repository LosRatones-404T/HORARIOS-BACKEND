from app.models import unsis
import app.models.models as models
from sqlalchemy.orm import Session

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
        models.ExamSpecifications.id == course_id
    ).first()


# guardar examen
def save_exam(db: Session, exam: models.Exam):
    db.add(exam)
    db.commit()
    db.refresh(exam)
    return exam


# para otro repo de datos de unsis #################
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

# obtener periodo actual de unsis
def get_current_unsis_period(db: Session):
    current_period = db.query(unsis.Periodo).order_by(unsis.Periodo.id.desc()).first()
    if current_period:
        return current_period.clave
    return None

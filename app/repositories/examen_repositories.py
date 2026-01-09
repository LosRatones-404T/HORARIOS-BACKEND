import app.models.models as models
from sqlalchemy.orm import Session

# obtener periodo actual de examenes
def get_current_exam_period(db: Session):
    # Suponiendo que hay una tabla o configuración que almacena el periodo actual
    current_period = db.query(models.periodos_examenes).order_by(models.periodos_examenes.id.desc()).first()
    if current_period:
        return current_period.nombre_periodo
    return None

# obtener todas las carreras
def get_all_degrees(db: Session):
    return db.query(models.Degree).all()

# obtener examenes generados por periodo
def get_exams_by_period(db: Session, period: str):
    return db.query(models.Exam).join(models.Course).filter(models.Course.period == period).all()

# obtener examenes generados por periodo y curso
def get_exams_by_period_and_course(db: Session, period: str, course_id: int):
    return db.query(models.Exam).join(models.Course).filter(models.Course.period == period, models.Exam.course_id == course_id).all()

# obtener examenes generados en el periodo de examenes actual
def get_exams_period(db: Session, period: str, exam_type: str):
    return db.query(models.Exam).join(models.Course).filter(models.Course.period == period, models.Exam.examen_type == exam_type).all()

# obtener especificaciones de examen por curso
def get_exam_especifications_by_course(db: Session, course_id: str):
    return db.query(models.exam_especifications).filter(models.exam_especifications.id == course_id).first()




# para otro repo     
# otener cursos por carrera
def get_courses_by_degree(db: Session, degree_id: int):
    return db.query(models.Course).filter(models.Course.degree_id == degree_id).all().orde

# obtener aulas
def get_all_classrooms(db: Session):
    return db.query(models.Classroom).all()

# guardar examen
def save_exam(db: Session, exam: models.Exam):
    db.add(exam)
    db.commit()
    db.refresh(exam)
    return exam
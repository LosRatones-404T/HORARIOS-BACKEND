from app.models import unsis
import app.models.models as models
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
def save_or_update_exam_specifications(db: Session, exam_spec: models.ExamSpecifications):
    existing_spec = db.query(models.ExamSpecifications).filter(
        models.ExamSpecifications.course_id == exam_spec.course_id
    ).first()
    if existing_spec:
        # Actualizar los campos necesarios
        existing_spec.tipo_examen = exam_spec.tipo_examen
        existing_spec.duracion_minutos = exam_spec.duracion_minutos
        existing_spec.requiere_sala_computo = exam_spec.requiere_sala_computo
        existing_spec.periodo_actual = exam_spec.periodo_actual
        db.commit()
        db.refresh(existing_spec)
        return existing_spec
    else:
        db.add(exam_spec)
        db.commit()
        db.refresh(exam_spec)
        return exam_spec   



def create_exam_spec(self, exam_data: ExamSpecCreate):
        # Convertimos el esquema Pydantic a Modelo SQLAlchemy
        # **exam_data.dict() desempaqueta los campos automáticamente
        db_exam = models.ExamSpecifications(**exam_data.dict())
        
        self.db.add(db_exam)
        self.db.commit()
        self.db.refresh(db_exam) # Obtiene el ID generado por la BD
        return db_exam

def get_by_materia(self, materia_id: str):
    return self.db.query(models.ExamSpecifications).filter(models.ExamSpecifications.materia_id == materia_id).all()
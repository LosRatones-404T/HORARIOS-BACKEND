from sqlalchemy.orm import Session
from app.models import models
from app.repositories.examen_repositories import save_exam,  get_exams_period, get_exam_especifications_by_course,  save_or_update_exam_specifications, get_current_exam_period
from app.repositories.unsis_repository import get_courses_by_degree, get_all_classrooms

def generate_exam_for_course(db: Session, id: str):
    """
    Genera un examen para un curso específico.
    
    Args:
        db: Sesión de base de datos
        id: ID del curso
        
    Returns:
        Exam: Objeto del examen generado o None si no se pudo generar
    """
    # Verificar especificaciones del examen antes de continuar
    exam_especifications = get_exam_especifications_by_course(db, id)
    if not exam_especifications:
        return None  # No hay especificaciones para este curso
    
    # Obtener datos necesarios
    current_period = get_current_exam_period()
    if not current_period:
        return None  # No hay período de exámenes activo
        
    exams = get_exams_period(db, current_period, exam_especifications.tipo_examen)
    classrooms = get_all_classrooms(db)
    
    if not classrooms:
        return None  # No hay aulas disponibles
    
    # Obtener fecha y horario del examen
    exam_date, start_time, end_time = obtener_time_exam(id, exam_especifications, exams)
    if exam_date is None:
        return None  # No hay disponibilidad de fecha/hora para este examen
    
    # Obtener aula para el examen (preferentemente la del curso regular)
    classroom_id = obtener_classroom_for_exam(id, exam_especifications, classrooms, exams)
    if classroom_id is None:
        return None  # No hay aulas disponibles para este examen
    
    # Crear el objeto del examen generado
    examen_generado = models.Exam(
        course_id=id,
        exam_date=exam_date,
        start_time=start_time,
        end_time=end_time,
        classroom_id=classroom_id,
        examen_type=exam_especifications.tipo_examen
    )
    
    # TODO: Implementar asignación de profesor
    # examen_generado.professor_id = obtener_professor_for_exam(id, exam_especifications)
    # if examen_generado.professor_id is None:
    #     return None  # No hay profesor disponible para este examen
    
    # TODO: Implementar verificación de estado del examen
    # examen_generado.status = status_exam(examen_generado)

    return examen_generado
    
    


def generate_exam_schedule_degree(db: Session, degree_id: str):
    courses = get_courses_by_degree(db, degree_id)

    exams_conflict = []
    exams_created = []

    for course in courses:
        exam_generate = generate_exam_for_course(db, course.id)
        if exam_generate is models.ScheduleConflict:
            exams_conflict.append(exam_generate)
        else:
            saved_exam = save_exam(db, exam_generate)
            exams_created.append(saved_exam)

    return exams_created


def classroom_available(db: Session, exam_date, start_time, end_time, classroom_id):
    
    pass  # Lógica para verificar si un aula está disponible en una fecha y hora específicas

def obtener_time_exam(course_id, exam_especifications, exams): #Si si se le asigna un horario al examen y se cambia en especifications, preferible horario de clase regular, asigna dia y hora, solo un examen por día
    pass  # Lógica para obtener la fecha y hora del examen

def obtener_classroom_for_exam(course_id, exam_especifications, classrooms, exams):
    pass  # Lógica para obtener el aula para el examen

def obtener_professor_for_exam(course_id, exam_especifications):
    pass  # Lógica para obtener el profesor para el examen



# Verifica si el estado del examen Realizado, en curso o Pendiente
def status_exam(exam: models.Exam):
    pass  # Lógica para determinar el estado del examen basado en la fecha y hora actual


# Llena reporte de examen generados
def fill_exam_report(exam_id: str):
    pass  # Lógica para llenar un reporte de exámenes generados
    reporte = models.GeneratedExamReport
    reporte.exam_id = exam_id
    
# def definir_preferencias_examen
def definir_preferencias_examen(course_id: str, preferences: dict):
    save_or_update_exam_specifications(course_id, preferences)
    pass  # Lógica para definir las preferencias del examen para un curso específico
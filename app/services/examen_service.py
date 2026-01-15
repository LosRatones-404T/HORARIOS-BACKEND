from sqlalchemy.orm import Session
from app.models import models
from app.repositories.examen_repositories import get_courses_by_degree, get_all_classrooms, save_exam, get_exams_by_period, get_exams_period, get_exam_especifications_by_course, get_current_exam_period

def generate_exam_for_course(db: Session, id: str):
    # Lógica para generar un examen para un curso específico
    # Datos necesarios
    exam_especifications = get_exam_especifications_by_course(db, id)
    classrooms = get_all_classrooms(db)
    exams = get_exams_period(db, get_current_exam_period(db), exam_especifications.tipo_examen)
    examen_generado = models.Exam(
        course_id=id,
        exam_date=None,
        start_time=None,
        end_time=None,
        classroom_id=None,
        examen_type=exam_especifications.tipo_examen
    )
    if not exam_especifications: # añadir condiciones para verificar si se realiza la generación, aulas disponibles, etc.
        return None  # No hay especificaciones para este curso
    

    examen_generado.exam_date, examen_generado.start_time, examen_generado.end_time = obtener_time_exam(id, exam_especifications, exams)
    if examen_generado.exam_date is None:
        return None  # No hay disponibilidad para este examen
    examen_generado.classroom_id = obtener_classroom_for_exam(id, exam_especifications, classrooms, exams)

    if obtener_classroom_for_exam(id, exam_especifications, classrooms, exams) is None: # Asignr aula preferentemente aula de clase regular
        return None  # No hay aulas disponibles para este examen
    
    # examen_generado.professor_id = obtener_professor_for_exam(id, exam_especifications)
    # if obtener_professor_for_exam(id, exam_especifications) is None: # Asignar profesor preferentemente el de la clase regular
    #     return None  # No hay profesor disponible para este examen
    
    # examen_generado.status = status_exam(examen_generado)

    return examen_generado
    
    


def generate_exam_schedule_degree(db: session, degree_id: str):
    courses = get_courses_by_degree(db, degree_id)

    exams_conflict = []
    exams_created = []

    for course in courses:
        exam_generate = generate_exam_for_course(course.id), 
        if exam_generate is models.ScheduleConflict:
            exams_conflict.append(exam_generate)
        else:
            saved_exam = save_exam(db, exam_generate)
            exams_created.append(saved_exam)

    return exams_created


def classroom_available(exam_date, start_time, end_time, classroom_id):
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
    

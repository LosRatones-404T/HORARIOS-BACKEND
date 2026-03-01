from sqlalchemy.orm import Session
from app.models import models, unsis
from app.repositories.examen_repositories import save_exam
from app.repositories.unsis_repository import get_exam_periods_dates
from datetime import datetime, time, date, timedelta
from typing import List, Tuple, Optional, Dict

# Horarios disponibles para exámenes parciales (1 hora)
HORARIOS_PARCIALES = [
    (time(8, 0), time(9, 0)),
    (time(9, 0), time(10, 0)),
    (time(10, 0), time(11, 0)),
    (time(11, 0), time(12, 0)),
    (time(12, 0), time(13, 0)),
    (time(13, 0), time(14, 0)),
    (time(16, 0), time(17, 0)),
    (time(17, 0), time(18, 0)),
]

# Horarios para ordinarios y extraordinarios (2 horas)
HORARIOS_ORDINARIOS_EXTRAORDINARIOS = [
    (time(8, 0), time(10, 0)),
    (time(10, 0), time(12, 0)),
    (time(12, 0), time(14, 0)),
    (time(16, 0), time(18, 0)),
]


def generar_fechas_disponibles(fecha_inicio: date, fecha_fin: date) -> List[date]:
    """Generar lista de fechas entre dos fechas (solo días de lunes a viernes)"""
    fechas = []
    current_date = fecha_inicio
    while current_date <= fecha_fin:
        # weekday(): 0=Lunes, 1=Martes, ..., 4=Viernes, 5=Sábado, 6=Domingo
        if current_date.weekday() < 5:  # Solo lunes a viernes
            fechas.append(current_date)
        current_date += timedelta(days=1)
    return fechas


def obtener_horarios_por_tipo_examen(tipo_examen: str) -> List[Tuple[time, time]]:
    """Obtener horarios según el tipo de examen"""
    # Parciales: 1 hora
    if tipo_examen in ["PRIMER_PARCIAL", "SEGUNDO_PARCIAL", "TERCER_PARCIAL"]:
        return HORARIOS_PARCIALES
    # Ordinarios y extraordinarios: 2 horas
    else:
        return HORARIOS_ORDINARIOS_EXTRAORDINARIOS


def obtener_capacidad_requerida(db: Session, materia_id: str) -> int:
    """Calcular capacidad requerida basándose en estudiantes inscritos"""
    grupos = db.query(unsis.Grupo).join(
        unsis.Horario, unsis.Horario.grupo_id == unsis.Grupo.clave
    ).filter(
        unsis.Horario.materia_id == materia_id
    ).all()
    
    total = sum(grupo.cupo for grupo in grupos if grupo.cupo)
    return total if total > 0 else 30


def verificar_disponibilidad_aula(
    db: Session,
    aula_id: str,
    exam_date: date,
    start_time: time,
    end_time: time,
    capacidad_requerida: int
) -> bool:
    """Verificar si un aula está disponible"""
    # Validar que no sea sábado ni domingo
    if exam_date.weekday() >= 5:
        return False
    
    aula = db.query(unsis.Aula).filter(unsis.Aula.clave == aula_id).first()
    if not aula or aula.capacidad < capacidad_requerida:
        return False
    
    # Verificar conflictos
    conflictos = db.query(models.Exam).filter(
        models.Exam.aula_id == aula_id,
        models.Exam.exam_date == exam_date,
        models.Exam.start_time < end_time,
        models.Exam.end_time > start_time
    ).count()
    
    return conflictos == 0


def verificar_disponibilidad_profesor(
    db: Session,
    profesor_id: str,
    exam_date: date,
    start_time: time,
    end_time: time
) -> bool:
    """Verificar disponibilidad del profesor"""
    if not profesor_id:
        return True
    
    # Validar que no sea sábado ni domingo
    if exam_date.weekday() >= 5:
        return False
    
    conflictos = db.query(models.Exam).filter(
        models.Exam.profesor_id == profesor_id,
        models.Exam.exam_date == exam_date,
        models.Exam.start_time < end_time,
        models.Exam.end_time > start_time
    ).count()
    
    return conflictos == 0


def obtener_aula_disponible(
    db: Session,
    tipo_aplicacion: str,
    exam_date: date,
    start_time: time,
    end_time: time,
    capacidad_requerida: int,
    preferencia_aula_id: Optional[str] = None
) -> Optional[str]:
    """Obtener un aula disponible"""
    # Validar que no sea fin de semana
    if exam_date.weekday() >= 5:
        return None
    
    # Intentar con preferencia
    if preferencia_aula_id:
        if verificar_disponibilidad_aula(db, preferencia_aula_id, exam_date, start_time, end_time, capacidad_requerida):
            return preferencia_aula_id
    
    # Buscar aulas por tipo
    query = db.query(unsis.Aula).filter(unsis.Aula.capacidad >= capacidad_requerida)
    
    if tipo_aplicacion == "COMPUTADORA":
        query = query.filter(unsis.Aula.tipo == "COMPUTADORA")
    else:
        query = query.filter((unsis.Aula.tipo == "AULA") | (unsis.Aula.tipo.is_(None)))
    
    aulas = query.order_by(unsis.Aula.capacidad).all()
    
    for aula in aulas:
        if verificar_disponibilidad_aula(db, aula.clave, exam_date, start_time, end_time, capacidad_requerida):
            return aula.clave
    
    return None


def generate_exam_for_course(
    db: Session,
    materia_id: str,
    tipo_examen: str,
    fechas_disponibles: List[date]
) -> Optional[models.Exam]:
    """Generar examen para una materia"""
    
    # Obtener especificaciones
    spec = db.query(models.ExamSpecification).filter(
        models.ExamSpecification.materia_id == materia_id,
        models.ExamSpecification.tipo_examen == tipo_examen
    ).first()
    
    if not spec:
        spec = models.ExamSpecification(
            materia_id=materia_id,
            tipo_examen=tipo_examen,
            tipo_aplicacion="ESCRITO",
            es_academia=False,
            duracion_minutos=60 if tipo_examen in ["PRIMER_PARCIAL", "SEGUNDO_PARCIAL", "TERCER_PARCIAL"] else 120
        )
    
    capacidad = obtener_capacidad_requerida(db, materia_id)
    horarios = obtener_horarios_por_tipo_examen(tipo_examen)
    
    # Buscar fecha y horario disponible (solo lunes a viernes)
    for fecha in fechas_disponibles:
        # Validación adicional: asegurar que sea día entre semana
        if fecha.weekday() >= 5:
            continue
            
        for start_time, end_time in horarios:
            # Verificar profesor
            if spec.profesor_aplicador_id:
                if not verificar_disponibilidad_profesor(db, spec.profesor_aplicador_id, fecha, start_time, end_time):
                    continue
            
            # Buscar aula
            aula_id = obtener_aula_disponible(
                db, spec.tipo_aplicacion, fecha, start_time, end_time,
                capacidad, spec.preferencia_aula_id
            )
            
            if aula_id:
                return models.Exam(
                    materia_id=materia_id,
                    aula_id=aula_id,
                    profesor_id=spec.profesor_aplicador_id,
                    exam_date=fecha,
                    start_time=start_time,
                    end_time=end_time,
                    examen_type=tipo_examen
                )
    
    return None


def generate_exam_schedule_degree(db: Session, degree_id: str, tipo_examen: str):
    """Generar horario de exámenes para una carrera"""
    
    periodos = get_exam_periods_dates(db)
    if not periodos or tipo_examen not in periodos:
        return {"success": False, "error": f"Periodo {tipo_examen} no configurado"}
    
    fecha_inicio, fecha_fin = periodos[tipo_examen]
    if not fecha_inicio or not fecha_fin:
        return {"success": False, "error": "Fechas no definidas"}
    
    fechas = generar_fechas_disponibles(fecha_inicio, fecha_fin)
    
    # Obtener materias de la carrera
    materias = db.query(unsis.Materia).join(
        unsis.Horario, unsis.Horario.materia_id == unsis.Materia.id
    ).join(
        unsis.Grupo, unsis.Grupo.clave == unsis.Horario.grupo_id
    ).filter(
        unsis.Grupo.carrera_id == degree_id
    ).distinct().all()
    
    examenes_creados = []
    examenes_conflicto = []
    
    for materia in materias:
        examen = generate_exam_for_course(db, materia.id, tipo_examen, fechas)
        
        if examen:
            try:
                db.add(examen)
                db.commit()
                db.refresh(examen)
                examenes_creados.append(examen)
            except Exception as e:
                db.rollback()
                examenes_conflicto.append({
                    "materia_id": materia.id,
                    "error": str(e)
                })
        else:
            examenes_conflicto.append({
                "materia_id": materia.id,
                "error": "No hay horarios disponibles"
            })
    
    return {
        "success": True,
        "examenes_creados": len(examenes_creados),
        "examenes_conflicto": len(examenes_conflicto),
        "detalles_conflictos": examenes_conflicto
    }


def generar_todos_los_examenes_carrera(db: Session, degree_id: str):
    """Generar todos los periodos de examen para una carrera"""
    tipos = ["PRIMER_PARCIAL", "SEGUNDO_PARCIAL", "TERCER_PARCIAL", 
             "ORDINARIO", "EXTRA_1", "EXTRA_2", "ESPECIAL"]
    
    resultados = {}
    for tipo in tipos:
        resultados[tipo] = generate_exam_schedule_degree(db, degree_id, tipo)
    
    return resultados
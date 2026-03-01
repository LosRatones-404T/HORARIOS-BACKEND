from datetime import date
from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.schemas.unsis_schemas import PeriodoResponse
from app.repositories import unsis_repository


def validate_period_dates(period: PeriodoResponse, current_period):
    """Validar que las fechas de parciales sean correctas"""
    
    # Validar que todas las fechas estén dentro del periodo
    fechas_a_validar = [
        ("Primer Parcial Inicio", period.primer_parcial_inicio),
        ("Primer Parcial Fin", period.primer_parcial_fin),
        ("Segundo Parcial Inicio", period.segundo_parcial_inicio),
        ("Segundo Parcial Fin", period.segundo_parcial_fin),
        ("Tercer Parcial Inicio", period.tercer_parcial_inicio),
        ("Tercer Parcial Fin", period.tercer_parcial_fin),
        ("Ordinario Inicio", period.ordinario_inicio),
        ("Ordinario Fin", period.ordinario_fin)
    ]
    
    for nombre, fecha in fechas_a_validar:
        if fecha and (fecha < current_period.fInicio or fecha > current_period.fFin):
            raise HTTPException(
                status_code=400,
                detail=f"{nombre} ({fecha}) debe estar dentro del periodo ({current_period.fInicio} - {current_period.fFin})"
            )
    
    # Validar orden y que no se solapen los periodos
    periodos = [
        ("Primer Parcial", period.primer_parcial_inicio, period.primer_parcial_fin),
        ("Segundo Parcial", period.segundo_parcial_inicio, period.segundo_parcial_fin),
        ("Tercer Parcial", period.tercer_parcial_inicio, period.tercer_parcial_fin),
        ("Ordinario", period.ordinario_inicio, period.ordinario_fin),
        ("Extra 1", period.extra1_inicio, period.extra1_fin),
        ("Extra 2", period.extra2_inicio, period.extra2_fin),
        ("Especial", period.especial_inicio, period.especial_fin),
    ]
    
    # Validar que fecha inicio sea menor que fecha fin en cada periodo
    for nombre, inicio, fin in periodos:
        if inicio and fin and inicio > fin:
            raise HTTPException(
                status_code=400,
                detail=f"{nombre}: la fecha de inicio ({inicio}) debe ser anterior a la fecha de fin ({fin})"
            )
    
    # Validar que los periodos no se solapen y vayan en orden
    fechas_fin_anteriores = []
    for nombre, inicio, fin in periodos:
        if inicio and fin:
            for fecha_fin_anterior in fechas_fin_anteriores:
                if inicio <= fecha_fin_anterior:
                    raise HTTPException(
                        status_code=400,
                        detail=f"{nombre} ({inicio} - {fin}) se solapa con un periodo anterior"
                    )
            fechas_fin_anteriores.append(fin)


def update_current_period(db: Session, period_update: PeriodoResponse):
    """Actualizar fechas de parciales del periodo actual"""
    current_period = unsis_repository.get_current_unsis_period(db)
    
    if not current_period:
        raise HTTPException(status_code=404, detail="No se encontró un periodo activo")
    
    # Validar fechas antes de actualizar
    validate_period_dates(period_update, current_period)
    
    # Si las validaciones pasan, actualizar en el repositorio
    return unsis_repository.update_current_period(db, period_update)
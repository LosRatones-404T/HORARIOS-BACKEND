from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.core.conexion import get_db
from app.schemas.degree_schemas import DegreeRead, DegreeCreate, DegreeUpdate, DegreeUpdateJefeCarrera, MessageResponse
from app.services import degree_service
from app.api.auth_routes import get_current_user
from app.models.models import User

router = APIRouter(
    prefix="/degrees",
    tags=["degrees"]
)


@router.get("/", response_model=List[DegreeRead])
def get_all_degrees(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Obtener todas las carreras.
    Roles permitidos: ADMIN, JEFE_CARRERA, JEFE_ESCOLARES, SECRETARIA
    """
    return degree_service.get_all_degrees(db)


@router.get("/active", response_model=List[DegreeRead])
def get_active_degrees(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Obtener solo las carreras activas.
    Roles permitidos: ADMIN, JEFE_CARRERA, JEFE_ESCOLARES, SECRETARIA
    """
    return degree_service.get_active_degrees(db)


@router.get("/{degree_id}", response_model=DegreeRead)
def get_degree_by_id(
    degree_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Obtener una carrera específica por ID.
    Roles permitidos: ADMIN, JEFE_CARRERA, JEFE_ESCOLARES, SECRETARIA
    """
    degree = degree_service.get_degree_by_id(db, degree_id)
    if not degree:
        raise HTTPException(status_code=404, detail="Carrera no encontrada")
    return degree


@router.post("/", response_model=DegreeRead, status_code=status.HTTP_201_CREATED)
def create_degree(
    degree_data: DegreeCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Crear una nueva carrera.
    Roles permitidos: ADMIN
    """
    if current_user.role not in ["ADMIN"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tienes permisos para crear carreras"
        )
    
    try:
        return degree_service.create_degree(db, degree_data)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.patch("/{degree_id}/jefe-carrera", response_model=DegreeRead)
def update_jefe_carrera(
    degree_id: str,
    jefe_data: DegreeUpdateJefeCarrera,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Actualizar el jefe de carrera en turno.
    Este endpoint permite cambiar qué profesor está actualmente como jefe de carrera,
    sin afectar los usuarios con rol JEFE_CARRERA del sistema.
    
    Roles permitidos: ADMIN, JEFE_CARRERA
    """
    if current_user.role not in ["ADMIN", "JEFE_CARRERA"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tienes permisos para actualizar el jefe de carrera"
        )
    
    try:
        return degree_service.update_jefe_carrera(db, degree_id, jefe_data)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.put("/{degree_id}/assign-user", response_model=DegreeRead)
def assign_user_to_degree(
    degree_id: str,
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Asignar un usuario del sistema como jefe de carrera.
    Este endpoint asigna un usuario con rol JEFE_CARRERA a una carrera específica.
    Solo puede haber un usuario asignado por carrera.
    
    Roles permitidos: ADMIN
    """
    if current_user.role != "ADMIN":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tienes permisos para asignar usuarios a carreras"
        )
    
    try:
        return degree_service.assign_jefe_carrera_user(db, degree_id, user_id)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.put("/{degree_id}", response_model=DegreeRead)
def update_degree(
    degree_id: str,
    degree_data: DegreeUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Actualizar una carrera completa.
    Roles permitidos: ADMIN
    """
    if current_user.role not in ["ADMIN"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tienes permisos para actualizar carreras"
        )
    
    try:
        return degree_service.update_degree(db, degree_id, degree_data)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.patch("/{degree_id}/toggle-status", response_model=DegreeRead)
def toggle_degree_status(
    degree_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Cambiar el estado activo/inactivo de una carrera.
    Roles permitidos: ADMIN
    """
    if current_user.role not in ["ADMIN"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tienes permisos para cambiar el estado de carreras"
        )
    
    try:
        return degree_service.toggle_degree_status(db, degree_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.delete("/{degree_id}", response_model=MessageResponse)
def delete_degree(
    degree_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Eliminar una carrera.
    Roles permitidos: ADMIN
    """
    if current_user.role not in ["ADMIN"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tienes permisos para eliminar carreras"
        )
    
    try:
        return degree_service.delete_degree(db, degree_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

from sqlalchemy.orm import Session
from app.repositories import degree_repository
from app.schemas.degree_schemas import DegreeCreate, DegreeUpdate, DegreeUpdateJefeCarrera


def get_all_degrees(db: Session):
    """Obtener todas las carreras"""
    return degree_repository.get_all_degrees(db)


def get_active_degrees(db: Session):
    """Obtener carreras activas"""
    return degree_repository.get_active_degrees(db)


def get_degree_by_id(db: Session, degree_id: str):
    """Obtener una carrera por ID"""
    return degree_repository.get_degree_by_id(db, degree_id)


def create_degree(db: Session, degree_data: DegreeCreate):
    """Crear una nueva carrera"""
    # Verificar si ya existe una carrera con el mismo nombre
    existing = degree_repository.get_degree_by_name(db, degree_data.name)
    if existing:
        raise ValueError("Ya existe una carrera con ese nombre")
    
    # Si se asigna un usuario, verificar que sea JEFE_CARRERA y no esté asignado a otra carrera
    if degree_data.jefe_carrera_user_id:
        from app.repositories.user_repository import get_user_by_id
        user = get_user_by_id(db, degree_data.jefe_carrera_user_id)
        if not user or user.role != "JEFE_CARRERA":
            raise ValueError("El usuario debe tener rol JEFE_CARRERA")
        
        # Verificar que el usuario no esté asignado a otra carrera
        existing_degree = degree_repository.get_all_degrees(db)
        for deg in existing_degree:
            if deg.jefe_carrera_user_id == degree_data.jefe_carrera_user_id:
                raise ValueError(f"El usuario ya está asignado a la carrera {deg.name}")
    
    return degree_repository.create_degree(
        db,
        id=degree_data.id,
        name=degree_data.name,
        jefe_carrera=degree_data.jefe_carrera,
        jefe_carrera_user_id=degree_data.jefe_carrera_user_id,
        is_active=degree_data.is_active
    )


def update_jefe_carrera(db: Session, degree_id: str, jefe_data: DegreeUpdateJefeCarrera):
    """Actualizar solo el jefe de carrera en turno"""
    degree = degree_repository.update_degree_jefe_carrera(db, degree_id, jefe_data.jefe_carrera)
    if not degree:
        raise ValueError("Carrera no encontrada")
    return degree


def update_degree(db: Session, degree_id: str, degree_data: DegreeUpdate):
    """Actualizar una carrera"""
    # Si se está actualizando el nombre, verificar que no exista otra carrera con ese nombre
    if degree_data.name:
        existing = degree_repository.get_degree_by_name(db, degree_data.name)
        if existing and existing.id != degree_id:
            raise ValueError("Ya existe otra carrera con ese nombre")
    
    # Si se asigna un usuario, verificar que sea JEFE_CARRERA y no esté asignado a otra carrera
    if degree_data.jefe_carrera_user_id:
        from app.repositories.user_repository import get_user_by_id
        user = get_user_by_id(db, degree_data.jefe_carrera_user_id)
        if not user or user.role != "JEFE_CARRERA":
            raise ValueError("El usuario debe tener rol JEFE_CARRERA")
        
        # Verificar que el usuario no esté asignado a otra carrera
        existing_degrees = degree_repository.get_all_degrees(db)
        for deg in existing_degrees:
            if deg.jefe_carrera_user_id == degree_data.jefe_carrera_user_id and deg.id != degree_id:
                raise ValueError(f"El usuario ya está asignado a la carrera {deg.name}")
    
    degree = degree_repository.update_degree(
        db,
        degree_id,
        name=degree_data.name,
        jefe_carrera=degree_data.jefe_carrera,
        jefe_carrera_user_id=degree_data.jefe_carrera_user_id,
        is_active=degree_data.is_active
    )
    if not degree:
        raise ValueError("Carrera no encontrada")
    return degree


def assign_jefe_carrera_user(db: Session, degree_id: str, user_id: int):
    """Asignar un usuario del sistema como jefe de carrera"""
    from app.repositories.user_repository import get_user_by_id
    
    user = get_user_by_id(db, user_id)
    if not user or user.role != "JEFE_CARRERA":
        raise ValueError("El usuario debe tener rol JEFE_CARRERA")
    
    # Verificar que el usuario no esté asignado a otra carrera
    existing_degrees = degree_repository.get_all_degrees(db)
    for deg in existing_degrees:
        if deg.jefe_carrera_user_id == user_id and deg.id != degree_id:
            raise ValueError(f"El usuario ya está asignado a la carrera {deg.name}")
    
    degree = degree_repository.assign_jefe_carrera_user(db, degree_id, user_id)
    if not degree:
        raise ValueError("Carrera no encontrada")
    return degree


def toggle_degree_status(db: Session, degree_id: str):
    """Cambiar el estado activo/inactivo de una carrera"""
    degree = degree_repository.toggle_degree_status(db, degree_id)
    if not degree:
        raise ValueError("Carrera no encontrada")
    return degree


def delete_degree(db: Session, degree_id: str):
    """Eliminar una carrera"""
    success = degree_repository.delete_degree(db, degree_id)
    if not success:
        raise ValueError("Carrera no encontrada")
    return {"message": "Carrera eliminada exitosamente"}

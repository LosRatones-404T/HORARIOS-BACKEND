from typing import Optional
from pydantic import BaseModel, ConfigDict


class UserInfo(BaseModel):
    """Información básica del usuario jefe de carrera"""
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    username: str
    email: Optional[str] = None
    is_active: bool


class DegreeBase(BaseModel):
    name: str
    jefe_carrera: Optional[str] = None  # Nombre del profesor en turno
    is_active: bool = True


class DegreeCreate(DegreeBase):
    id: str  # ID de la carrera (ejemplo: "ISC", "IE", "IM")
    jefe_carrera_user_id: Optional[int] = None  # ID del usuario del sistema


class DegreeUpdate(BaseModel):
    name: Optional[str] = None
    jefe_carrera: Optional[str] = None  # Nombre del profesor
    jefe_carrera_user_id: Optional[int] = None  # ID del usuario
    is_active: Optional[bool] = None


class DegreeUpdateJefeCarrera(BaseModel):
    """Schema para actualizar solo el jefe de carrera en turno"""
    jefe_carrera: str


class DegreeRead(DegreeBase):
    model_config = ConfigDict(from_attributes=True)
    
    id: str
    jefe_carrera_user_id: Optional[int] = None
    jefe_carrera_user: Optional[UserInfo] = None  # Usuario del sistema asignado


class MessageResponse(BaseModel):
    message: str

from typing import Optional
from enum import Enum
from pydantic import BaseModel, EmailStr, ConfigDict


class RoleEnum(str, Enum):
    ADMIN = "ADMIN"
    JEFE_CARRERA = "JEFE_CARRERA"
    JEFE_ESCOLARES = "JEFE_ESCOLARES"
    SECRETARIA = "SECRETARIA"


class DegreeInfo(BaseModel):
    """Información básica de la carrera"""
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    name: str
    jefe_carrera: Optional[str] = None
    is_active: bool


class UserCreate(BaseModel):
    username: str = "admin"
    email: Optional[EmailStr] = "j.lopezlopez1004@gmail.com"
    password: str = "admin123" 
    role: RoleEnum = RoleEnum.ADMIN

class UserCreateJefe(BaseModel):
    username: str = "INFORMATICA"
    email: Optional[EmailStr] = "informatica@unsis.edu.mx"
    password: str = "info123" 
    role: RoleEnum = RoleEnum.JEFE_CARRERA
    carrera: str = "06B"


class UserRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    username: str
    email: Optional[EmailStr] = None
    role: RoleEnum
    is_active: bool


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Optional[str] = None


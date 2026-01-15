# schemas/sync_schemas.py
from pydantic import BaseModel
from typing import Optional
from datetime import date

# Nota: Define los campos tal cual vienen en el JSON
class PeriodoSchema(BaseModel):
    clave: str
    nombre: str
    tipo: str
    fInicio: date
    fFin: date

class CarreraSchema(BaseModel):
    clave: str
    nombre: str
    vigente: bool

class GrupoSchema(BaseModel):
    clave: str
    nombre: str
    semestre: int
    alumnos: int
    carrera: str  # En el JSON viene como "carrera", aunque sea una FK
    periodo: str  # En el JSON viene como "periodo"

class AulaSchema(BaseModel):
    clave: str
    nombre: str
    capacidad: int
    tipo: str
    statusProyector: Optional[str] = None
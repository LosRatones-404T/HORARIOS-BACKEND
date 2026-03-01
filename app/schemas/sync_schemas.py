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

class HorarioItemSchema(BaseModel):
    rowId: int
    dia: int
    hora: int
    
    # IDs para relaciones
    idGrupo: str
    idAula: Optional[str] = None # A veces puede venir null o vacío
    idprofesor: Optional[str] = None
    asignatura: str # ID de la materia
    
    # Campos de texto para guardar en tablas catalogo (Profesor/Materia)
    nombreCompleto: Optional[str] = None
    materia: str # Nombre de la materia
    
    # Campos que ignoraremos porque ya los tenemos por relación (nombreGrupo, nombreAula, carrera, etc.)
from datetime import date
from pydantic import BaseModel
from typing import Optional
# Este es el molde de cómo se verá el JSON de cada grupo
class GrupoResponse(BaseModel):
    clave: str
    nombre: str
    semestre: int
    alumnos: int
    carrera_id: str  # O el nombre que uses en tu modelo
    periodo_id: str

    class Config:
        # Esto es vital: le dice a Pydantic que lea los datos desde el objeto ORM de SQLAlchemy
        from_attributes = True

# Schema para Aulas
class AulaResponse(BaseModel):
    clave: str
    nombre: str
    capacidad: int
    tipo: str
    statusProyector: Optional[str] = None

    class Config:
        from_attributes = True

# Schema para Carreras
class CarreraResponse(BaseModel):
    clave: str
    nombre: str
    vigente: bool

    class Config:
        from_attributes = True

# Schema para Periodo de Exámenes (fusionado con Periodo de Unsis)
class PeriodoResponse(BaseModel):
    clave: str
    nombre: str
    tipo: str
    fInicio: date
    fFin: date
    
    # Periodos de Exámenes
    # Primer Parcial
    primer_parcial_inicio: Optional[date] = None
    primer_parcial_fin: Optional[date] = None
    
    # Segundo Parcial
    segundo_parcial_inicio: Optional[date] = None
    segundo_parcial_fin: Optional[date] = None
    
    # Tercer Parcial
    tercer_parcial_inicio: Optional[date] = None
    tercer_parcial_fin: Optional[date] = None
    
    # Ordinario
    ordinario_inicio: Optional[date] = None
    ordinario_fin: Optional[date] = None
    
    # Extraordinario
    extra1_inicio: Optional[date] = None
    extra1_fin: Optional[date] = None

    # Extraordinario 2
    extra2_inicio: Optional[date] = None
    extra2_fin: Optional[date] = None

    class Config:
        from_attributes = True

# # Mantener PeriodoExamenResponse para compatibilidad con endpoint /current-period
class PeriodoExamenResponse(BaseModel):
    id: int
    nombre_periodo: str
    
    # Primer Parcial
    primer_parcial_inicio: Optional[str] = None
    primer_parcial_fin: Optional[str] = None
    
    # Segundo Parcial
    segundo_parcial_inicio: Optional[str] = None
    segundo_parcial_fin: Optional[str] = None
    
    # Tercer Parcial
    tercer_parcial_inicio: Optional[str] = None
    tercer_parcial_fin: Optional[str] = None
    
    # Ordinario
    ordinario_inicio: Optional[str] = None
    ordinario_fin: Optional[str] = None
    
    # Extraordinario
    extraordinario_inicio: Optional[str] = None
    extraordinario_fin: Optional[str] = None

    class Config:
        from_attributes = True

# Schema para Materias
class MateriaResponse(BaseModel):
    id: str
    nombre: str

    class Config:
        from_attributes = True

# Schema para Horarios
class HorarioResponse(BaseModel):
    id: int
    dia: int  # 1=Lunes, 2=Martes, etc.
    hora: int  # Hora en formato entero
    grupo_id: str
    aula_id: Optional[str] = None
    profesor_id: Optional[str] = None
    materia_id: str

    class Config:
        from_attributes = True

# Schema para Profesores
class ProfesorResponse(BaseModel):
    id: str
    nombre: str

    class Config:
        from_attributes = True
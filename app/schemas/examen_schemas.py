from pydantic import BaseModel
from datetime import date, time

class ExamResponse(BaseModel):
    id: int
    course: str      # Nombre de la materia
    group: str       # Grupo (ej. 106-A)
    professor: str   # Nombre del profe
    classroom: str   # Aula asignada
    date: date       # Fecha del examen
    start: time      # Hora inicio
    end: time        # Hora fin

    class Config:
        # Esto permite que Pydantic lea datos directamente de los modelos de SQLAlchemy
        from_attributes = True

class MessageResponse(BaseModel):
    message: str

    class Config:
        from_attributes = True

class ExamSpecCreate(BaseModel):
    course_id: int  # ID de la materia/curso para el cual es la especificación
    tipo_examen: str  # "parcial" o "ordinario"
    duracion_minutos: int
    requiere_sala_computo: bool = False
    periodo_actual: str

# Esquema para responder (Output) - Incluye el ID generado
class ExamSpecResponse(ExamSpecCreate):
    id: int

    class Config:
        from_attributes = True  # Antes orm_mode = True
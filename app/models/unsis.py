from typing import Optional, List
from datetime import date
from sqlalchemy import String, Integer, Boolean, Date, ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.core.conexion import Base

# 1. Modelo de Carreras (carreras.json)
class Carrera(Base):
    __tablename__ = "carreras"

    # La 'clave' (ej: "06B") es la llave primaria
    clave: Mapped[str] = mapped_column(String(10), primary_key=True)
    nombre: Mapped[str] = mapped_column(String(200))
    vigente: Mapped[bool] = mapped_column(Boolean, default=True)

    # Relación inversa: Una carrera tiene muchos grupos
    grupos: Mapped[List["Grupo"]] = relationship(back_populates="carrera_rel")

# 2. Modelo de Periodo (periodo_actual.json)
class Periodo(Base):
    __tablename__ = "periodos"

    clave: Mapped[str] = mapped_column(String(10), primary_key=True) # Ej: "2526A"
    nombre: Mapped[str] = mapped_column(String(100))
    tipo: Mapped[str] = mapped_column(String(5))      # Ej: "A"
    fInicio: Mapped[date] = mapped_column(Date)       # Mapear "2025-10-01"
    fFin: Mapped[date] = mapped_column(Date)
    
    # Periodos de Exámenes
    # Primer Parcial
    primer_parcial_inicio: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    primer_parcial_fin: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    
    # Segundo Parcial
    segundo_parcial_inicio: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    segundo_parcial_fin: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    
    # Tercer Parcial
    tercer_parcial_inicio: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    tercer_parcial_fin: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    
    # Ordinario
    ordinario_inicio: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    ordinario_fin: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    
    # Extraordinario
    extraordinario_inicio: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    extraordinario_fin: Mapped[Optional[date]] = mapped_column(Date, nullable=True)

    # Relación: Un periodo tiene muchos grupos
    grupos: Mapped[List["Grupo"]] = relationship(back_populates="periodo_rel")

# 3. Modelo de Aulas (aulas.json)
class Aula(Base):
    __tablename__ = "aulas"

    clave: Mapped[str] = mapped_column(String(10), primary_key=True) # Ej: "1", "95"
    nombre: Mapped[str] = mapped_column(String(50))   # Ej: "A1", "LAB INFO"
    capacidad: Mapped[int] = mapped_column(Integer)
    tipo: Mapped[str] = mapped_column(String(50))     # Ej: "AULA", "LABORATORIO"
    
    # Puede ser nulo según tu JSON (null, "", "SI", "NO_FUNCIONA")
    statusProyector: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)

# 4. Modelo de Grupos (grupos.json)
class Grupo(Base):
    __tablename__ = "grupos"

    # Clave compuesta o ID propio? El JSON tiene "clave": "104-A", usaremos esa.
    clave: Mapped[str] = mapped_column(String(20), primary_key=True)
    nombre: Mapped[str] = mapped_column(String(50))
    semestre: Mapped[int] = mapped_column(Integer)
    alumnos: Mapped[int] = mapped_column(Integer)

    # Claves foráneas (Foreign Keys)
    # Apuntan a las tablas carreras y periodos
    carrera_id: Mapped[str] = mapped_column(ForeignKey("carreras.clave"))
    periodo_id: Mapped[str] = mapped_column(ForeignKey("periodos.clave"))

    # Relaciones para navegar en Python (ej: mi_grupo.carrera_rel.nombre)
    carrera_rel: Mapped["Carrera"] = relationship(back_populates="grupos")
    periodo_rel: Mapped["Periodo"] = relationship(back_populates="grupos")


class Profesor(Base):
    __tablename__ = "profesores"
    
    # idprofesor en el JSON (ej: "1154", "T7")
    id: Mapped[str] = mapped_column(String(20), primary_key=True)
    nombre: Mapped[str] = mapped_column(String(200)) # nombreCompleto

class Materia(Base):
    __tablename__ = "materias"
    
    # asignatura en el JSON (ej: "4016_2017")
    id: Mapped[str] = mapped_column(String(20), primary_key=True)
    nombre: Mapped[str] = mapped_column(String(200)) # materia

class Horario(Base):
    __tablename__ = "horarios"

    # Usamos el rowId del JSON como primaria para facilitar actualizaciones exactas
    id: Mapped[int] = mapped_column(Integer, primary_key=True) 
    
    dia: Mapped[int] = mapped_column(Integer) # 1=Lunes, 2=Martes...
    hora: Mapped[int] = mapped_column(Integer) # Formato entero: 13, 14, 8...
    
    # Claves Foráneas
    grupo_id: Mapped[str] = mapped_column(ForeignKey("grupos.clave"))
    aula_id: Mapped[str] = mapped_column(ForeignKey("aulas.clave"), nullable=True)
    profesor_id: Mapped[str] = mapped_column(ForeignKey("profesores.id"), nullable=True)
    materia_id: Mapped[str] = mapped_column(ForeignKey("materias.id"))

    # Relaciones
    grupo = relationship("Grupo")
    aula = relationship("Aula")
    profesor = relationship("Profesor")
    materia = relationship("Materia")

    # Constraint opcional: Un profesor no puede estar en dos lugares a la misma hora y día
    # __table_args__ = (
    #     UniqueConstraint('profesor_id', 'dia', 'hora', name='uq_profesor_dia_hora'),
    # )
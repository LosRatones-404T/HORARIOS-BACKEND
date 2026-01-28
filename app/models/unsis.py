from typing import Optional, List
from datetime import date
from sqlalchemy import String, Integer, Boolean, Date, ForeignKey
from sqlalchemy.dialects.postgresql import JSONB  # Importar JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.core.conexion import Base

class Carrera(Base):
    __tablename__ = "carreras"
    __table_args__ = {'schema': 'unsis'}

    clave: Mapped[str] = mapped_column(String(10), primary_key=True)
    nombre: Mapped[str] = mapped_column(String(200))
    vigente: Mapped[bool] = mapped_column(Boolean, default=True)

    grupos: Mapped[List["Grupo"]] = relationship(back_populates="carrera_rel")


class Periodo(Base):
    __tablename__ = "periodos"
    __table_args__ = {'schema': 'unsis'}

    clave: Mapped[str] = mapped_column(String(10), primary_key=True)
    nombre: Mapped[str] = mapped_column(String(100))
    tipo: Mapped[str] = mapped_column(String(5))
    fInicio: Mapped[date] = mapped_column(Date)
    fFin: Mapped[date] = mapped_column(Date)
    
    primer_parcial_inicio: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    primer_parcial_fin: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    
    segundo_parcial_inicio: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    segundo_parcial_fin: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    
    tercer_parcial_inicio: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    tercer_parcial_fin: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    
    ordinario_inicio: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    ordinario_fin: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    
    extra1_inicio: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    extra1_fin: Mapped[Optional[date]] = mapped_column(Date, nullable=True)

    extra2_inicio: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    extra2_fin: Mapped[Optional[date]] = mapped_column(Date, nullable=True)

    especial_inicio: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    especial_fin: Mapped[Optional[date]] = mapped_column(Date, nullable=True)

    grupos: Mapped[List["Grupo"]] = relationship(back_populates="periodo_rel")


class Aula(Base):
    __tablename__ = "aulas"
    __table_args__ = {'schema': 'unsis'}

    clave: Mapped[str] = mapped_column(String(10), primary_key=True)
    nombre: Mapped[str] = mapped_column(String(50))
    capacidad: Mapped[int] = mapped_column(Integer)
    tipo: Mapped[str] = mapped_column(String(50))
    statusProyector: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)


class Grupo(Base):
    __tablename__ = "grupos"
    __table_args__ = {'schema': 'unsis'}

    clave: Mapped[str] = mapped_column(String(20), primary_key=True)
    nombre: Mapped[str] = mapped_column(String(50))
    semestre: Mapped[int] = mapped_column(Integer)
    cupo: Mapped[int] = mapped_column(Integer, nullable=True)

    carrera_id: Mapped[str] = mapped_column(ForeignKey("unsis.carreras.clave"))
    periodo_id: Mapped[str] = mapped_column(ForeignKey("unsis.periodos.clave"))

    # Usar JSONB en lugar de JSON
    alumnos: Mapped[Optional[dict]] = mapped_column(JSONB, nullable=True)
    datos_adicionales: Mapped[Optional[dict]] = mapped_column(JSONB, nullable=True)

    carrera_rel: Mapped["Carrera"] = relationship(back_populates="grupos")
    periodo_rel: Mapped["Periodo"] = relationship(back_populates="grupos")


class Profesor(Base):
    __tablename__ = "profesores"
    __table_args__ = {'schema': 'unsis'}
    
    id: Mapped[str] = mapped_column(String(20), primary_key=True)
    nombre: Mapped[str] = mapped_column(String(200))


class Materia(Base):
    __tablename__ = "materias"
    __table_args__ = {'schema': 'unsis'}
    
    id: Mapped[str] = mapped_column(String(20), primary_key=True)
    nombre: Mapped[str] = mapped_column(String(200))


class Horario(Base):
    __tablename__ = "horarios"
    __table_args__ = {'schema': 'unsis'}

    id: Mapped[int] = mapped_column(Integer, primary_key=True) 
    
    dia: Mapped[int] = mapped_column(Integer)
    hora: Mapped[int] = mapped_column(Integer)
    
    grupo_id: Mapped[str] = mapped_column(ForeignKey("unsis.grupos.clave"))
    aula_id: Mapped[Optional[str]] = mapped_column(ForeignKey("unsis.aulas.clave"), nullable=True)
    profesor_id: Mapped[Optional[str]] = mapped_column(ForeignKey("unsis.profesores.id"), nullable=True)
    materia_id: Mapped[str] = mapped_column(ForeignKey("unsis.materias.id"))

    grupo = relationship("Grupo")
    aula = relationship("Aula")
    profesor = relationship("Profesor")
    materia = relationship("Materia")
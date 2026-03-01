from email.policy import default
from sqlalchemy import Column, Text, Integer, String, Boolean, ForeignKey, Date, Time, DateTime, func
from sqlalchemy.orm import relationship
from app.core.conexion import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True, nullable=False)
    email = Column(String(120), unique=True, index=True, nullable=True)
    hashed_password = Column(String, nullable=False)
    role = Column(String(50), nullable=False, default="user")
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class Exam(Base):
    __tablename__ = "examens"
    
    id = Column(Integer, primary_key=True, index=True)
    materia_id = Column(String, nullable=False)
    grupo_id = Column(String, nullable=True)
    aula_id = Column(String, nullable=True)
    profesor_id = Column(String, nullable=True)
    exam_date = Column(Date, nullable=False)
    start_time = Column(Time, nullable=False)
    end_time = Column(Time, nullable=False)
    examen_type = Column(String, nullable=False, default="PRIMER_PARCIAL")
    is_active = Column(Boolean, default=True)
    
    examen_time_generated = Column(DateTime(timezone=True), server_default=func.now())
    generated_by_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    
    generated_by = relationship("User", foreign_keys=[generated_by_id])


class ExamSpecification(Base):
    __tablename__ = "exam_specifications"
    
    id = Column(Integer, primary_key=True, index=True,default=0)
    materia_id = Column(String, nullable=False, default="")
    grupo_id = Column(String, nullable=True, default="")
    tipo_examen = Column(String, nullable=False, default="PRIMER_PARCIAL")
    tipo_aplicacion = Column(String, nullable=False, default="ESCRITO") # COMPUTADORA O ESCRITO
    es_academia = Column(Boolean, default=False)
    profesor_aplicador_id = Column(String, nullable=True) # MISMO QUE IMPARTE LA MATERIA
    duracion_minutos = Column(Integer, default=120)
    preferencia_aula_id = Column(String, nullable=True) # MISMA QUE CLASE NORMAL
    notas = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())


class ScheduleConflict(Base):
    __tablename__ = "schedule_conflicts"

    id = Column(Integer, primary_key=True, index=True)
    exam_id_1 = Column(Integer, ForeignKey("examens.id"), nullable=False)
    exam_id_2 = Column(Integer, ForeignKey("examens.id"), nullable=False)
    conflict_type = Column(String, nullable=False)
    reason = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    exam1 = relationship("Exam", foreign_keys=[exam_id_1])
    exam2 = relationship("Exam", foreign_keys=[exam_id_2])


class GeneratedExamReport(Base):
    __tablename__ = "generated_exam_reports"

    id = Column(Integer, primary_key=True, index=True)
    carrera_id = Column(String, nullable=False)
    tipo_examen = Column(String, nullable=False)
    total_examenes = Column(Integer, default=0)
    examenes_exitosos = Column(Integer, default=0)
    examenes_con_conflicto = Column(Integer, default=0)
    generated_by_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    generated_at = Column(DateTime(timezone=True), server_default=func.now())
    details = Column(Text, nullable=True)
    
    generated_by = relationship("User")
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Date, Time, DateTime, func
from sqlalchemy.orm import relationship
from app.core.conexion import Base


class Classroom(Base):
    __tablename__ = "classrooms"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    capacity = Column(Integer, default=30)
    is_computer_lab = Column(Boolean, default=False)
    


class Professor(Base):
    __tablename__ = "professors"
    
    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String, index=True, nullable=False)
    external_id = Column(String, unique=True, nullable=True) 


class Course(Base):
    __tablename__ = "courses"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, nullable=False)
    group_name = Column(String, index=True, nullable=False)
    semester = Column(Integer, nullable=False)
    professor_id = Column(Integer, ForeignKey("professors.id"))
    cluster_id = Column(Integer, nullable=True, index=True)

    professor = relationship("Professor", backref="courses")
    regular_schedules = relationship("RegularSchedule", back_populates="course", cascade="all, delete-orphan")
    exam = relationship("Exam", uselist=False, back_populates="course")


class RegularSchedule(Base):
    __tablename__ = "regular_schedules"
    
    id = Column(Integer, primary_key=True, index=True)
    course_id = Column(Integer, ForeignKey("courses.id"))
    day_of_week = Column(Integer)
    start_time = Column(Time)
    end_time = Column(Time)
    
    course = relationship("Course", back_populates="regular_schedules")


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
    course_id = Column(Integer, ForeignKey("courses.id"), unique=True)
    classroom_id = Column(Integer, ForeignKey("classrooms.id"))
    exam_date = Column(Date)
    start_time = Column(Time)
    end_time = Column(Time)
    examen_type = Column(String, nullable=False, default="parcial")
    is_active = Column(Boolean, default=False)
    
    examen_time_generated = Column(DateTime(timezone=True))
    
    generated_by_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    examen_generated_by = relationship("User", foreign_keys=[generated_by_id])
    
    course = relationship("Course", back_populates="exam")
    classroom = relationship("Classroom")


class Degree(Base):
    __tablename__ = "degrees"

    id = Column(String, primary_key=True, index=True)
    name = Column(String, unique=True, index=True, nullable=False)
    jefe_carrera = Column(String, nullable=True)
    jefe_carrera_user_id = Column(Integer, ForeignKey("users.id"), unique=True, nullable=True)
    is_active = Column(Boolean, default=True)
    
    jefe_carrera_user = relationship("User", backref="degree_managed", foreign_keys=[jefe_carrera_user_id])

class ExamSpecifications(Base):
    __tablename__ = "exam_specifications"

    id = Column(Integer, primary_key=True, index=True)
    course_id = Column(Integer, ForeignKey("courses.id"), nullable=False, unique=True)
    tipo_examen = Column(String, nullable=False)
    duracion_minutos = Column(Integer, nullable=False)
    requiere_sala_computo = Column(Boolean, default=False)
    periodo_actual = Column(String, nullable=False)
    
    course = relationship("Course", backref="exam_specifications")

class ScheduleConflict(Base):
    __tablename__ = "schedule_conflicts"

    id = Column(Integer, primary_key=True, index=True)
    course_id_1 = Column(Integer, ForeignKey("courses.id"), nullable=False)
    course_id_2 = Column(Integer, ForeignKey("courses.id"), nullable=False)
    reason = Column(String, nullable=True)

class GeneratedExamReport(Base):
    __tablename__ = "generated_exam_reports"

    id = Column(Integer, primary_key=True, index=True)
    course_id = Column(Integer, ForeignKey("courses.id"), nullable=False)
    exam_id = Column(Integer, ForeignKey("examens.id"), nullable=False)
    status = Column(String, nullable=False)
    same_aula = Column(Boolean, default=False)
    same_time = Column(Boolean, default=False)
    details = Column(String, nullable=True)

class PeriodosExamenes(Base):
    __tablename__ = "exam_periods"

    id = Column(Integer, primary_key=True, index=True)
    nombre_periodo = Column(String, unique=True, nullable=False)  # Ej: "2024-A", "2024-B"
    
    # Primer Parcial
    primer_parcial_inicio = Column(Date, nullable=True)
    primer_parcial_fin = Column(Date, nullable=True)
    
    # Segundo Parcial
    segundo_parcial_inicio = Column(Date, nullable=True)
    segundo_parcial_fin = Column(Date, nullable=True)
    
    # Tercer Parcial
    tercer_parcial_inicio = Column(Date, nullable=True)
    tercer_parcial_fin = Column(Date, nullable=True)
    
    # Ordinario
    ordinario_inicio = Column(Date, nullable=True)
    ordinario_fin = Column(Date, nullable=True)
    
    # Extraordinario
    extraordinario_inicio = Column(Date, nullable=True)
    extraordinario_fin = Column(Date, nullable=True)


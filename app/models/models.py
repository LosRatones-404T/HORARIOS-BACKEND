from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Date, Time, DateTime, func
from sqlalchemy.orm import relationship
from app.core.conexion import Base


# 1. Modelo de Aula (Ya lo tenías, lo dejo por referencia)
class Classroom(Base):
    __tablename__ = "classrooms"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True) # Ej: "F3", "CETI-S.O."
    capacity = Column(Integer, default=30)
    is_computer_lab = Column(Boolean, default=False) # Para saber si es sala de cómputo
    




# 3. Modelo de Materia (EL NÚCLEO)
class Course(Base):
    __tablename__ = "courses"
    
    id = Column(Integer, primary_key=True, index=True)
    
    # Datos Básicos
    name = Column(String, index=True, nullable=False)       # Ej: "Cálculo I"
    group_name = Column(String, index=True, nullable=False) # Ej: "106-A"
    semester = Column(Integer, nullable=False)               # Ej: 1, 3, 5 (Opcional, útil para filtrar)
    
    # Relaciones (Foreign Keys)
    professor_id = Column(Integer, ForeignKey("professors.id"))
    
    # CLAVE PARA TU REQUERIMIENTO:
    # Si "Matemáticas 104A" y "Matemáticas 104B" deben presentar juntas,
    # ambas deben tener el mismo número aquí (ej: 100).
    # El algoritmo buscará materias con el mismo cluster_id para agendarlas igual.
    cluster_id = Column(Integer, nullable=True, index=True)

    # Definición de Relaciones para SQLAlchemy
    professor = relationship("Professor", backref="courses")
    
    # Una materia tiene MUCHOS horarios de clase (Lunes 9am, Miercoles 11am...)
    # cascade="all, delete-orphan" significa que si borras la materia, se borran sus horarios.
    regular_schedules = relationship("RegularSchedule", back_populates="course", cascade="all, delete-orphan")
    
    # Una materia tiene UN solo examen final/parcial agendado
    exam = relationship("Exam", uselist=False, back_populates="course")


# 4. Horarios Habituales (Para la preferencia de horario)
class RegularSchedule(Base):
    __tablename__ = "regular_schedules"
    
    id = Column(Integer, primary_key=True, index=True)
    course_id = Column(Integer, ForeignKey("courses.id"))
    
    day_of_week = Column(Integer) # 0=Lunes, 1=Martes... 6=Domingo
    start_time = Column(Time)     # Ej: 09:00:00
    end_time = Column(Time)       # Ej: 10:00:00
    
    # Opcional: Si se quiere recordar en qué aula toman clase normalmente
    # classroom_id = Column(Integer, ForeignKey("classrooms.id"), nullable=True) 
    
    course = relationship("Course", back_populates="regular_schedules")


# 5. El Examen Generado
class Exam(Base):
    __tablename__ = "examens"
    
    id = Column(Integer, primary_key=True, index=True)
    
    # Relaciones
    course_id = Column(Integer, ForeignKey("courses.id"), unique=True)
    classroom_id = Column(Integer, ForeignKey("classrooms.id"))
    
    # Datos del Examen
    exam_date = Column(Date)
    start_time = Column(Time)
    end_time = Column(Time)

    examen_type = Column(String, nullable=False, default="parcial") # "ordinario" o "parcial"

    is_active = Column(Boolean, default=False) # generar función si el examen esta activo o no, lo revisa en base al exameen date y startr
    
    examen_time_generated = Column(DateTime(timezone=True))
    id_generated_by = Column(Integer, ForeignKey("users.id"))  # Usuario que generó el examen
    examen_generated_by = relationship("User", back_populates ="generated_exams")  # Usuario que generó el examen
    course = relationship("Course", back_populates="exam")
    classroom = relationship("Classroom")


# 2. Modelo de Profesor
class Professor(Base):
    __tablename__ = "professors"
    
    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String, index=True, nullable=False)
    # ID externo por si sincronizas con otro sistema de la universidad
    external_id = Column(String, unique=True, nullable=True) 


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True, nullable=False)
    email = Column(String(120), unique=True, index=True, nullable=True)
    hashed_password = Column(String, nullable=False)
    role = Column(String(50), nullable=False, default="user")
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    generated_exams1 = relationship("Exam", back_populates="examen_generated_by")

class Degree(Base):
    __tablename__ = "degrees"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True, nullable=False)
    jefe_carrera = Column(String, nullable=True)
    is_active = Column(Boolean, default=True)

# Especificaciones para examen
class ExamSpecifications(Base):
    __tablename__ = "exam_specifications"

    id = Column(Integer, primary_key=True, index=True) # tal vez utilizar course_id como PK
    tipo_examen = Column(String, nullable=False)  # Ej: "parcial", "ordinario"
    duracion_minutos = Column(Integer, nullable=False)  # Duración del examen en minutos
    requiere_sala_computo = Column(Boolean, default=False)  # Si el examen requiere sala de cómputo
    periodo_actual = Column(String, nullable=False)  # Ej: "Enero 2024"

# Conflicto en generacion de horarios
class ScheduleConflict(Base):
    __tablename__ = "schedule_conflicts"

    id = Column(Integer, primary_key=True, index=True)
    course_id_1 = Column(Integer, ForeignKey("courses.id"), nullable=False)
    course_id_2 = Column(Integer, ForeignKey("courses.id"), nullable=False)
    reason = Column(String, nullable=True)  # Razón del conflicto

# Informe de examen generado
class GeneratedExamReport(Base):
    __tablename__ = "generated_exam_reports"

    id = Column(Integer, primary_key=True, index=True)
    course_id = Column(Integer, ForeignKey("courses.id"), nullable=False)
    exam_id = Column(Integer, ForeignKey("examens.id"), nullable=False)
    status = Column(String, nullable=False)  # Ej: "created", "conflict"
    same_aula = Column(Boolean, default=False)  # Si se logró mantener el mismo aula
    same_time = Column(Boolean, default=False)  # Si se logró mantener el mismo horario que clase regular
    details = Column(String, nullable=True)  # Detalles adicionales sobre la generación

class PeriodosExamenes(Base):
    __tablename__ = "exam_periods"

    id = Column(Integer, primary_key=True, index=True)
    nombre_periodo = Column(String, unique=True, nullable=False)  # Ej: "Enero 2024"
    fecha_inicio = Column(Date, nullable=False)
    fecha_fin = Column(Date, nullable=False)
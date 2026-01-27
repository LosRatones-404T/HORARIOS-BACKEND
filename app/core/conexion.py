from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv
import logging

# Desactivar logs de SQLAlchemy
logging.getLogger('sqlalchemy.engine').setLevel(logging.WARNING)

# Cargar variables de entorno
load_dotenv()

# Obtener URL de la base de datos
DATABASE_URL = os.getenv("DATABASE_URL")

# Crear el motor de SQLAlchemy
engine = create_engine(
    DATABASE_URL,
    echo=False,  # No mostrar las consultas SQL en consola
    pool_pre_ping=True,  # Verifica la conexión antes de usarla
    pool_size=5,  # Número de conexiones en el pool
    max_overflow=10  # Conexiones adicionales si se necesitan
)

# Crear sesión local
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

# Base para los modelos
Base = declarative_base()


# Función para crear las tablas en la BD
def create_tables():
    """Crea todas las tablas definidas en los modelos"""
    # Importar todos los modelos para que sean registrados por SQLAlchemy
    from app.models import models, unsis
    Base.metadata.create_all(bind=engine)


# Función para verificar conexión
def test_connection():
    """Prueba la conexión a la base de datos"""
    try:
        with engine.connect() as connection:
            print("Conexión exitosa a la base de datos")
            return True
    except Exception as e:
        print(f"Error de conexión: {e}")
        return False


# Dependency generator para FastAPI: abrir y cerrar sesiones correctamente
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
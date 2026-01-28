from sqlalchemy import create_engine, event, text
from sqlalchemy.orm import sessionmaker, declarative_base
from app.core.config import settings
import logging

logger = logging.getLogger(__name__)

# Crear el engine de SQLAlchemy
engine = create_engine(
    settings.DATABASE_URL,
    pool_pre_ping=True,
    echo=False,
    pool_size=10,
    max_overflow=20
)

# Crear la sesión
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base para los modelos
Base = declarative_base()

def get_db():
    """Dependency para obtener la sesión de base de datos"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def create_tables():
    """Crea todas las tablas definidas en los modelos"""
    try:
        # Crear el schema 'unsis' si no existe
        with engine.connect() as conn:
            conn.execute(text("CREATE SCHEMA IF NOT EXISTS unsis"))
            conn.commit()
            logger.info("Schema 'unsis' verificado/creado")
        
        # Importar todos los modelos para que SQLAlchemy los conozca
        from app.models import models, unsis
        
        # Crear todas las tablas
        Base.metadata.create_all(bind=engine)
        logger.info("Tablas creadas exitosamente")
    except Exception as e:
        logger.error(f"Error creando tablas: {e}")
        raise

def test_connection():
    """Prueba la conexión a la base de datos"""
    try:
        with engine.connect() as connection:
            connection.execute(text("SELECT 1"))
        logger.info("Conexión exitosa a la base de datos")
        return True
    except Exception as e:
        logger.error(f"Error conectando a la base de datos: {e}")
        return False
from venv import create
from warnings import deprecated
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.conexion import test_connection, create_tables, SessionLocal
from app.api import examen_routes
from app.api.auth_routes import router as auth_router
import app.models.models as models
import logging

# Configurar nivel de logging
logging.getLogger("uvicorn").setLevel(logging.WARNING)
logging.getLogger("uvicorn.access").setLevel(logging.WARNING)

from passlib.context import CryptContext

# Configuración de hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Configuración de FastAPI con root_path para Nginx
app = FastAPI(
    title="Siplex API",
    description="API para gestión horarios de examenes",
    version="1.0.0",
    root_path="/api"
)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:8080",
        "http://132.18.38.133:8080"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def startup_event():
    print("Iniciando Siplex API...")
    
    if test_connection():
        print("Base de datos conectada")
        create_tables()

        # Lógica para crear usuario ADMIN automático
        db = SessionLocal()
        try:
            user_count = db.query(models.User).count()
            if user_count == 0:
                print("No hay usuarios. Creando administrador inicial...")
                admin_user = models.User(
                    username="admin",
                    email="admin@siplex.unsis.edu.mx",
                    hashed_password=pwd_context.hash("admin123"),
                    role="ADMIN",
                    is_active=True
                )
                db.add(admin_user)
                db.commit()
                print("Usuario 'admin' creado exitosamente")
            else:
                print(f"Usuarios en base de datos: {user_count}. Omitiendo creacion inicial.")
        except Exception as e:
            print(f"Error al crear usuario inicial: {e}")
            db.rollback()
        finally:
            db.close()

        print("\nRutas disponibles:")
        print("   -> http://localhost:8080/api")
        print("   -> http://localhost:8080/api/docs")
        print("   -> http://localhost:8080/api/health\n")
    else:
        print("Error: No se pudo conectar a la base de datos")

@app.on_event("shutdown")
async def shutdown_event():
    print("Cerrando aplicacion...")

@app.get("/")
def root():
    return {
        "message": "API de Horarios funcionando",
        "version": "1.0.0",
        "status": "Online"
    }

@app.get("/health")
def health():
    return {"status": "healthy", "database": "connected"}

# Registro de Routers
app.include_router(auth_router)
app.include_router(examen_routes.router)

from app.api.sync_routes import router as sync_router
app.include_router(sync_router)

from app.api.unsis_routes import router as unsis_router
app.include_router(unsis_router)

from app.api.users_routes import router as users_router
app.include_router(users_router)

from app.api.degree_routes import router as degree_router
app.include_router(degree_router)
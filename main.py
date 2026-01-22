from venv import create
from warnings import deprecated
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.conexion import test_connection, create_tables
from app.api import examen_routes
from app.api.auth_routes import router as auth_router
import app.models.models as models # Asegura que los modelos se registren

# importar sesión para crear usuario inicial
from app.core.conexion import SessionLocal
from passlib.context import CryptContext

# Configuración de hashing para crear usuario demo
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# Crear la aplicación FastAPI
app = FastAPI(
    title="Horarios API",
    description="API para gestión horarios de examenes",
    version="1.0.0"
)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Evento al iniciar la aplicación
@app.on_event("startup")
async def startup_event():
    """Se ejecuta cuando inicia el servidor"""
    print("Iniciando aplicación...")
    
    # Verificar conexión a la BD
    if test_connection():
        print("Base de datos conectada")
        
        # Crear tablas si no existen
        create_tables()
        """
        # Crear usuario ADMIN por defecto si no existe ningun usuario
        db = SessionLocal()
        try:
            user_count = db.query(models.User).count()
            print(user_count)
            if user_count == 0:
                print("No hay usuarios en la base de datos. Creando usuario por defecto...")
                admin_user = models.User(
                    username="admin",
                    email="unsis.siplex.unsis.edu.mx",
                    hashed_password=pwd_context.hash("admin123"),
                    role="admin",
                    is_active = True
                )
                db.add(admin_user)
                db.commit()
                print("Usuario 'admin' creado con contraseña 'admin123'")
            else:
                print(f"Usuarios existentes en la base de datos: {user_count}. No se crea usuario por defecto.")
        
        
        except Exception as e:
            print(f"Error al crear usuario por defecto: {e}")
        finally:
            db.close()

        """


        print("\nRutas disponibles:")
        print("   → http://localhost:8000")
        print("   → http://localhost:8000/docs")
        print("   → http://localhost:8000/health\n")
    else:
        print("Error: No se pudo conectar a la base de datos")

# Evento al cerrar la aplicación
@app.on_event("shutdown")
async def shutdown_event():
    """Se ejecuta cuando se cierra el servidor"""
    print("Cerrando aplicación...")

# Ruta de prueba
@app.get("/")
def root():
    return {
        "message": "API de Horarios funcionando",
        "version": "1.0.0",
        "status": "Online"
    }

# Ruta de health check
@app.get("/health")
def health():
    return {
        "status": "healthy",
        "database": "connected"
    }


# Registrar routers adicionales
app.include_router(auth_router)
app.include_router(examen_routes.router)


# Importar y registrar el router de sincronización
from app.api.sync_routes import router as sync_router
app.include_router(sync_router)

# importar y registrar el router de unsis
from app.api.unsis_routes import router as unsis_router
app.include_router(unsis_router)

# importar y registrar el router de usuarios
from app.api.users_routes import router as users_router
app.include_router(users_router)

# importar y registrar el router de carreras
from app.api.degree_routes import router as degree_router
app.include_router(degree_router)
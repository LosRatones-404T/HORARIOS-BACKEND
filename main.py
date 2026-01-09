
from fastapi import FastAPI
from app.core.conexion import test_connection, create_tables
from app.api import examen_routes
from app.api.auth_routes import router as auth_router

# Crear la aplicación FastAPI
app = FastAPI(
    title="Horarios API",
    description="API para gestión de exámenes y horarios",
    version="1.0.0"
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
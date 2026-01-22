# Sistema de Gestión de Horarios y Exámenes

API REST para la gestión automatizada de horarios de exámenes académicos con integración a UNSIS.

## 🚀 Inicio Rápido

### Docker (Recomendado)

```bash
docker-compose up --build -d
```

La API estará disponible en http://localhost:8000

### Desarrollo Local

1. Levantar base de datos:
```bash
docker-compose up -d postgres-horarios
```

2. Instalar dependencias:
```bash
poetry install
```

3. Ejecutar aplicación:
```bash
uvicorn main:app --reload
```

## 📁 Estructura del Proyecto

```
HORARIOS-BACKEND/
├── app/
│   ├── api/              # Endpoints REST
│   │   ├── auth_routes.py
│   │   ├── degree_routes.py
│   │   ├── examen_routes.py
│   │   ├── sync_routes.py
│   │   ├── unsis_routes.py
│   │   └── users_routes.py
│   ├── core/             # Configuración y seguridad
│   │   ├── config.py
│   │   ├── conexion.py
│   │   └── security.py
│   ├── models/           # Modelos de base de datos
│   │   ├── models.py
│   │   └── unsis.py
│   ├── repositories/     # Capa de acceso a datos
│   ├── schemas/          # Validación con Pydantic
│   └── services/         # Lógica de negocio
├── docs/                 # Documentación detallada
├── migrations/           # Migraciones de BD
├── tests/                # Pruebas automatizadas
├── docker-compose.yml
├── Dockerfile
├── main.py
├── pyproject.toml
└── README.md
```

## 🔑 Características Principales

### Autenticación y Autorización
- Sistema JWT con tokens de acceso
- Roles: `ADMIN`, `JEFE_CARRERA`, `JEFE_ESCOLARES`, `SECRETARIA`
- Control de acceso basado en roles (RBAC)
- Gestión de usuarios y permisos

### Gestión de Carreras
- CRUD completo de carreras académicas
- IDs alfanuméricos (ISC, IE, IM, etc.)
- Relación uno-a-uno: un usuario JEFE_CARRERA por carrera
- Campo `jefe_carrera` para nombre del profesor en turno
- Campo `jefe_carrera_user_id` para usuario del sistema

### Gestión de Exámenes
- Programación automatizada de exámenes
- Asignación inteligente de aulas
- Gestión de conflictos de horarios
- Especificaciones por materia (duración, requisitos)
- Períodos de exámenes (parciales, ordinarios, extraordinarios)

### Sincronización UNSIS
- Integración con sistema UNSIS
- Sincronización de carreras, materias, grupos y aulas
- Actualización bidireccional de datos

## 📖 Documentación

### Interfaces Web
- **Swagger UI:** http://localhost:8000/docs
- **ReDoc:** http://localhost:8000/redoc
- **OpenAPI JSON:** http://localhost:8000/openapi.json

### Documentación Detallada
- [API Reference](docs/API.md) - Endpoints completos con ejemplos
- [Gestión de Carreras](docs/DEGREES.md) - Sistema de carreras y jefaturas
- [Integración Usuario-Carrera](docs/USER_DEGREE_INTEGRATION.md) - Relaciones y flujos
- [Guía del Consumidor](docs/CONSUMER.md) - Uso desde frontend
- [Migraciones](migrations/README.md) - Historial de cambios en BD

## 🗄️ Base de Datos

**PostgreSQL 15** con dos esquemas:
- **public:** Sistema principal (usuarios, carreras, exámenes)
- **unsis:** Sincronización con UNSIS (materias, grupos, aulas)

### Migraciones Aplicadas
1. `001_add_degree_id_to_users.sql` - Relación User→Degree (revertida)
2. `002_reverse_user_degree_relationship.sql` - Relación Degree→User (actual)
3. `003_change_degree_id_to_varchar.sql` - IDs alfanuméricos para carreras

## 🔧 Configuración

### Variables de Entorno (.env)
```bash
DATABASE_URL=postgresql://user_horarios:horarios123@localhost:5433/horarios_db
POSTGRES_USER=user_horarios
POSTGRES_PASSWORD=horarios123
POSTGRES_SERVER=localhost
POSTGRES_PORT=5433
POSTGRES_DB=horarios_db
SECRET_KEY=tu_clave_secreta_aqui
ACCESS_TOKEN_EXPIRE_MINUTES=60
```

## 🧪 Testing

```bash
# Ejecutar todos los tests
pytest

# Tests específicos
pytest tests/test_auth.py
pytest tests/test_examenes.py

# Con cobertura
pytest --cov=app --cov-report=html
```

## 🛠️ Tecnologías

- **FastAPI** 0.115+ - Framework web moderno
- **SQLAlchemy** 2.0+ - ORM para Python
- **Pydantic** 2.0+ - Validación de datos
- **PostgreSQL** 15 - Base de datos relacional
- **Docker** - Contenedorización
- **Poetry** - Gestión de dependencias
- **JWT** - Autenticación sin estado
- **Uvicorn** - Servidor ASGI

## 📝 Ejemplos de Uso

### Autenticación
```bash
# Registrar usuario
curl -X POST http://localhost:8000/auth/register \
  -H "Content-Type: application/json" \
  -d '{"username":"demo","email":"demo@example.com","password":"Pass123","role":"SECRETARIA"}'

# Login
curl -X POST http://localhost:8000/auth/login \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=demo&password=Pass123"

# Obtener perfil
curl http://localhost:8000/auth/me \
  -H "Authorization: Bearer <TOKEN>"
```

### Gestión de Carreras
```bash
# Crear carrera
curl -X POST http://localhost:8000/degrees/ \
  -H "Authorization: Bearer <TOKEN>" \
  -H "Content-Type: application/json" \
  -d '{"id":"ISC","name":"Ingeniería en Sistemas Computacionales","is_active":true}'

# Listar carreras
curl http://localhost:8000/degrees/ \
  -H "Authorization: Bearer <TOKEN>"

# Asignar usuario a carrera
curl -X PUT http://localhost:8000/degrees/ISC/assign-user?user_id=2 \
  -H "Authorization: Bearer <TOKEN>"
```

## 🤝 Contribución

1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

## 📄 Licencia

Este proyecto es de uso interno para UNSIS.

## 👥 Equipo

Desarrollado para el sistema de gestión académica UNSIS.

## 📞 Soporte

Para reportar problemas o solicitar features, abre un issue en el repositorio.
# Resumen de Cambios: Relación Usuario-Carrera

## Fecha: 2024

## Objetivo
Cambiar el modelo de relación entre usuarios y carreras de **User → Degree (muchos a uno)** a **Degree → User (uno a uno)**.

## Razón del Cambio
El usuario requería que:
- Exista **UN solo usuario JEFE_CARRERA** por carrera
- El campo `jefe_carrera` (nombre del profesor) pueda cambiar independientemente del usuario del sistema
- Los usuarios del sistema con rol JEFE_CARRERA sean constantes, solo cambie el profesor en turno

## Cambios Realizados

### 1. Modelos (app/models/models.py)
**Eliminado de User:**
```python
degree_id = Column(Integer, ForeignKey("degrees.id"), nullable=True)
degree = relationship("Degree", back_populates="users")
```

**Agregado a Degree:**
```python
jefe_carrera_user_id = Column(Integer, ForeignKey("users.id"), unique=True, nullable=True)
jefe_carrera_user = relationship("User", backref="degree_managed", foreign_keys=[jefe_carrera_user_id])
```

### 2. Schemas

**app/schemas/user_schemas.py:**
- Eliminado `degree_id` de `UserCreate`
- Eliminado `degree_id` y `degree` de `UserRead`

**app/schemas/degree_schemas.py:**
- Agregado `UserInfo` schema para información básica del usuario
- Agregado `jefe_carrera_user_id` a `DegreeCreate` y `DegreeUpdate`
- Agregado `jefe_carrera_user` (UserInfo) a `DegreeRead`

### 3. Repositories

**app/repositories/user_repository.py:**
- Eliminada función `assign_degree_to_user`
- Eliminada función `get_users_by_degree`
- Agregada función `get_degree_managed_by_user`
- Actualizada función `create_user` (removido parámetro `degree_id`)

**app/repositories/degree_repository.py:**
- Actualizada función `create_degree` (agregado parámetro `jefe_carrera_user_id`)
- Actualizada función `update_degree` (agregado parámetro `jefe_carrera_user_id`)
- Agregada función `assign_jefe_carrera_user`

### 4. Services

**app/services/user_service.py:**
- Eliminada función `assign_degree_to_user`
- Eliminada función `get_users_by_degree`
- Agregada función `get_degree_managed_by_user`
- Actualizada función `register_user` (removido parámetro `degree_id`)

**app/services/degree_service.py:**
- Actualizada función `create_degree` con validaciones para `jefe_carrera_user_id`
- Actualizada función `update_degree` con validaciones para `jefe_carrera_user_id`
- Agregada función `assign_jefe_carrera_user`

**Validaciones agregadas:**
- Verificar que el usuario tiene rol JEFE_CARRERA
- Verificar que el usuario no está asignado a otra carrera
- Solo ADMIN puede asignar usuarios a carreras

### 5. API Routes

**app/api/users_routes.py:**
- Eliminado endpoint `PUT /users/assign-degree`
- Eliminado endpoint `GET /users/by-degree/{degree_id}`
- Agregado endpoint `GET /users/me/degree` (obtener carrera del usuario actual)

**app/api/degree_routes.py:**
- Agregado endpoint `PUT /degrees/{degree_id}/assign-user` (asignar usuario a carrera)

### 6. Base de Datos

**Migración 002_reverse_user_degree_relationship.sql:**
- Eliminado `users.degree_id` y constraints relacionados
- Agregado `degrees.jefe_carrera_user_id` con UNIQUE constraint
- Creado FK de `degrees.jefe_carrera_user_id` → `users.id`
- Creado índice en `jefe_carrera_user_id`

### 7. Documentación

**Archivos actualizados:**
- `docs/USER_DEGREE_INTEGRATION.md` - Reescrito completamente
- `migrations/README.md` - Reescrito completamente

**Archivos creados:**
- `migrations/002_reverse_user_degree_relationship.sql`
- `migrations/002_reverse_user_degree_relationship.py`
- `migrations/verify_migration.sh`
- `CHANGES_SUMMARY.md` (este archivo)

## Nuevos Endpoints

### Asignar Usuario a Carrera
```
PUT /degrees/{degree_id}/assign-user?user_id={user_id}
Rol requerido: ADMIN
```

### Obtener Carrera del Usuario Actual
```
GET /users/me/degree
Rol requerido: JEFE_CARRERA
```

## Endpoints Eliminados

```
PUT /users/assign-degree
GET /users/by-degree/{degree_id}
```

## Flujo de Trabajo Actualizado

1. **Crear usuario JEFE_CARRERA:**
```bash
POST /auth/register
{
  "username": "jefe_sistemas",
  "email": "jefe@sistemas.edu",
  "password": "password123",
  "role": "JEFE_CARRERA"
}
```

2. **Crear carrera:**
```bash
POST /degrees/
{
  "name": "Ingeniería en Sistemas",
  "jefe_carrera": "Dr. Juan Pérez",
  "jefe_carrera_user_id": 5,  # Opcional
  "is_active": true
}
```

3. **Asignar usuario a carrera (si no se hizo en creación):**
```bash
PUT /degrees/1/assign-user?user_id=5
```

4. **Usuario consulta su carrera:**
```bash
GET /users/me/degree
```

5. **Cambiar profesor en turno (no afecta al usuario):**
```bash
PATCH /degrees/1/jefe-carrera
{
  "jefe_carrera": "Dra. María López"
}
```

## Ventajas del Nuevo Diseño

1. **Separación Clara:**
   - Usuario del sistema → Autenticación y permisos
   - Nombre del profesor → Información para documentos

2. **Integridad Garantizada:**
   - Un usuario solo puede ser jefe de una carrera (UNIQUE constraint)
   - Un carrera solo puede tener un usuario asignado

3. **Flexibilidad:**
   - Cambiar el profesor en turno sin afectar permisos
   - Reasignar usuarios cuando sea necesario

4. **Seguridad:**
   - Validaciones a nivel de servicio y base de datos
   - Permisos claros por rol

## Verificación

Para verificar que los cambios se aplicaron correctamente:

```bash
# Ejecutar script de verificación
./migrations/verify_migration.sh

# Verificar que no hay column degree_id en users
docker exec postgres-horarios psql -U user_horarios -d horarios_db -c "\d users"

# Verificar que existe column jefe_carrera_user_id en degrees
docker exec postgres-horarios psql -U user_horarios -d horarios_db -c "\d degrees"
```

## Rollback

Si es necesario revertir los cambios:

```bash
# Opción 1: Usando script Python
python migrations/002_reverse_user_degree_relationship.py --rollback

# Opción 2: Usando SQL manual (ver migrations/README.md)
```

## Archivos Modificados

### Código Fuente
- ✅ app/models/models.py
- ✅ app/schemas/user_schemas.py
- ✅ app/schemas/degree_schemas.py
- ✅ app/repositories/user_repository.py
- ✅ app/repositories/degree_repository.py
- ✅ app/services/user_service.py
- ✅ app/services/degree_service.py
- ✅ app/api/users_routes.py
- ✅ app/api/degree_routes.py

### Base de Datos
- ✅ migrations/002_reverse_user_degree_relationship.sql
- ✅ migrations/002_reverse_user_degree_relationship.py

### Documentación
- ✅ docs/USER_DEGREE_INTEGRATION.md
- ✅ migrations/README.md
- ✅ CHANGES_SUMMARY.md

### Scripts de Utilidad
- ✅ migrations/verify_migration.sh

## Estado del Sistema

**Antes de los cambios:**
- User.degree_id → Degree.id (muchos a uno)
- Múltiples usuarios podían tener la misma carrera

**Después de los cambios:**
- Degree.jefe_carrera_user_id → User.id (uno a uno, UNIQUE)
- Solo un usuario puede gestionar cada carrera
- El nombre del profesor (jefe_carrera) es independiente del usuario del sistema

## Próximos Pasos

1. ✅ Refactoring completado
2. ✅ Migración de base de datos aplicada
3. ✅ Documentación actualizada
4. ⏳ Probar endpoints en ambiente de desarrollo
5. ⏳ Actualizar tests si existen
6. ⏳ Deploy a producción

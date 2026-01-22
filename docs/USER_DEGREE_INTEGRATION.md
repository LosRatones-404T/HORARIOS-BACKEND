# Integración Usuario-Carrera

## Descripción General

Este documento describe cómo funciona la integración entre usuarios (especialmente con rol `JEFE_CARRERA`) y las carreras en el sistema de gestión de horarios.

## Modelo de Datos

### Relación Degree → User (Uno a Uno)

Cada carrera puede tener **UN único usuario** del sistema asignado como JEFE_CARRERA. Esta relación se gestiona mediante:

**Tabla `degrees`:**
- `jefe_carrera` (VARCHAR): Nombre del profesor que está actualmente en turno como jefe de carrera
- `jefe_carrera_user_id` (INTEGER, UNIQUE): FK al usuario del sistema con permisos de JEFE_CARRERA

**Tabla `users`:**
- No tiene referencia a carreras directamente
- Los usuarios con rol `JEFE_CARRERA` pueden ser asignados a una carrera mediante `degrees.jefe_carrera_user_id`

### Restricciones Importantes

1. **Unicidad**: Un usuario solo puede ser jefe de UNA carrera (constraint UNIQUE en `jefe_carrera_user_id`)
2. **Rol Requerido**: Solo usuarios con rol `JEFE_CARRERA` pueden ser asignados a carreras
3. **Independencia**: El campo `jefe_carrera` (nombre del profesor) puede cambiar independientemente del usuario del sistema

## Casos de Uso

### Caso 1: Asignar Usuario a Carrera

**Endpoint:** `PUT /degrees/{degree_id}/assign-user`

**Request:**
```bash
curl -X PUT "http://localhost:8000/degrees/1/assign-user?user_id=5" \
  -H "Authorization: Bearer <admin_token>"
```

**Validaciones:**
- El usuario debe existir y tener rol `JEFE_CARRERA`
- El usuario no debe estar asignado a otra carrera
- Solo usuarios `ADMIN` pueden realizar esta operación

**Respuesta:**
```json
{
  "id": 1,
  "name": "Ingeniería en Sistemas",
  "jefe_carrera": "Dr. Juan Pérez López",
  "jefe_carrera_user_id": 5,
  "jefe_carrera_user": {
    "id": 5,
    "username": "jefe_sistemas",
    "email": "jefe@sistemas.edu",
    "is_active": true
  },
  "is_active": true,
  "created_at": "2024-01-15T10:00:00"
}
```

### Caso 2: Cambiar Profesor en Turno

**Endpoint:** `PATCH /degrees/{degree_id}/jefe-carrera`

**Request:**
```bash
curl -X PATCH "http://localhost:8000/degrees/1/jefe-carrera" \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{"jefe_carrera": "Dr. Juan Pérez López"}'
```

**Nota:** Esto solo cambia el nombre del profesor, NO afecta al usuario del sistema.

### Caso 3: Autenticación de Jefe de Carrera

Cuando un usuario con rol `JEFE_CARRERA` se autentica, puede consultar su carrera asignada:

**Endpoint:** `GET /users/me/degree`

**Request:**
```bash
curl -X GET "http://localhost:8000/users/me/degree" \
  -H "Authorization: Bearer <jefe_carrera_token>"
```

**Respuesta:**
```json
{
  "id": 1,
  "name": "Ingeniería en Sistemas",
  "jefe_carrera": "Dr. Juan Pérez López",
  "jefe_carrera_user_id": 5,
  "jefe_carrera_user": {
    "id": 5,
    "username": "jefe_sistemas",
    "email": "jefe@sistemas.edu",
    "is_active": true
  },
  "is_active": true,
  "created_at": "2024-01-15T10:00:00"
}
```

Si el usuario no tiene carrera asignada:
```json
{
  "message": "No tienes una carrera asignada"
}
```

## Flujo de Trabajo Típico

### 1. Crear Usuario JEFE_CARRERA

```bash
POST /auth/register
{
  "username": "jefe_sistemas",
  "email": "jefe@sistemas.edu",
  "password": "password123",
  "role": "JEFE_CARRERA"
}
```

### 2. Crear Carrera (con o sin usuario asignado)

**Con usuario asignado:**
```bash
POST /degrees/
{
  "name": "Ingeniería en Sistemas",
  "jefe_carrera": "Dr. Juan Pérez López",
  "jefe_carrera_user_id": 5,
  "is_active": true
}
```

**Sin usuario asignado:**
```bash
POST /degrees/
{
  "name": "Ingeniería en Sistemas",
  "jefe_carrera": "Dr. Juan Pérez López",
  "is_active": true
}
```

### 3. Asignar Usuario a Carrera (si no se hizo en creación)

```bash
PUT /degrees/1/assign-user?user_id=5
```

### 4. Usuario se Autentica y Consulta su Carrera

```bash
# Login
POST /auth/login
{
  "username": "jefe_sistemas",
  "password": "password123"
}

# Con el token obtenido, consultar carrera
GET /users/me/degree
```

## Diferencias Importantes

### Campo `jefe_carrera` vs Usuario del Sistema

Es fundamental entender la diferencia:

| Concepto | Campo | Descripción | Se Puede Cambiar |
|----------|-------|-------------|------------------|
| **Nombre del Profesor** | `degree.jefe_carrera` | Nombre del profesor actualmente en turno | ✅ Sí, frecuentemente |
| **Usuario del Sistema** | `degree.jefe_carrera_user_id` | Usuario con permisos de login y gestión | ⚠️ Sí, pero raramente |

**Ejemplo:**
- El Dr. Juan Pérez es jefe de carrera de Enero a Junio → `jefe_carrera = "Dr. Juan Pérez"`
- La Dra. María López toma el puesto de Julio a Diciembre → `jefe_carrera = "Dra. María López"`
- El usuario del sistema `jefe_sistemas` se mantiene igual para ambos periodos

## Endpoints Disponibles

### Gestión de Carreras

| Método | Endpoint | Descripción | Rol Requerido |
|--------|----------|-------------|---------------|
| `GET` | `/degrees/` | Listar todas las carreras | Autenticado |
| `GET` | `/degrees/{id}` | Obtener carrera específica | Autenticado |
| `POST` | `/degrees/` | Crear nueva carrera | ADMIN |
| `PUT` | `/degrees/{id}` | Actualizar carrera completa | ADMIN |
| `PATCH` | `/degrees/{id}/jefe-carrera` | Cambiar nombre del jefe en turno | ADMIN, JEFE_CARRERA |
| `PUT` | `/degrees/{id}/assign-user` | Asignar usuario del sistema | ADMIN |
| `DELETE` | `/degrees/{id}` | Eliminar carrera | ADMIN |

### Gestión de Usuarios

| Método | Endpoint | Descripción | Rol Requerido |
|--------|----------|-------------|---------------|
| `GET` | `/users/jefes-carrera` | Listar usuarios JEFE_CARRERA | Autenticado |
| `GET` | `/users/me/degree` | Obtener carrera del usuario actual | JEFE_CARRERA |

## Ventajas de este Diseño

### 1. Separación de Responsabilidades
- **Usuario del sistema:** Maneja autenticación y permisos
- **Nombre del profesor:** Información para reportes y documentos oficiales

### 2. Flexibilidad
- Cambiar el profesor en turno sin afectar permisos del sistema
- Reasignar usuarios a diferentes carreras cuando sea necesario
- Un mismo usuario puede gestionar diferentes carreras en diferentes momentos

### 3. Seguridad
- Solo un usuario puede gestionar cada carrera a la vez (UNIQUE constraint)
- Permisos claros y bien definidos a nivel de base de datos
- Foreign keys garantizan integridad referencial

### 4. Integridad de Datos
- Constraints a nivel de base de datos garantizan consistencia
- UNIQUE constraint previene asignación duplicada
- ON DELETE SET NULL previene errores al eliminar usuarios

## Validaciones

### Al Crear/Actualizar Carrera con Usuario

```python
# El servicio valida:
1. El usuario existe
2. El usuario tiene rol JEFE_CARRERA
3. El usuario no está asignado a otra carrera
4. Solo ADMIN puede hacer esta operación
```

### Al Asignar Usuario a Carrera

```python
# El servicio valida:
1. La carrera existe
2. El usuario existe y tiene rol JEFE_CARRERA
3. El usuario no está ya asignado a otra carrera
4. Solo ADMIN puede hacer esta operación
```

## Migraciones

La relación actual fue establecida por la migración `002_reverse_user_degree_relationship.sql` que:
- Eliminó `users.degree_id` y sus constraints
- Agregó `degrees.jefe_carrera_user_id` con UNIQUE constraint
- Creó FK de `degrees.jefe_carrera_user_id` → `users.id` con ON DELETE SET NULL
- Creó índice en `degrees.jefe_carrera_user_id` para rendimiento

Para más detalles sobre migraciones, ver [migrations/README.md](../migrations/README.md)

## Ejemplos Completos

### Ejemplo 1: Setup Completo de Nueva Carrera

```bash
# 1. Crear usuario JEFE_CARRERA
curl -X POST http://localhost:8000/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "username": "jefe_industrial",
    "email": "jefe@industrial.edu",
    "password": "SecurePass123",
    "role": "JEFE_CARRERA"
  }'

# 2. Login como ADMIN
curl -X POST http://localhost:8000/auth/login \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=admin&password=admin123"

# 3. Crear carrera con usuario asignado
curl -X POST http://localhost:8000/degrees/ \
  -H "Authorization: Bearer <admin_token>" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Ingeniería Industrial",
    "jefe_carrera": "Dra. Ana Martínez Gómez",
    "jefe_carrera_user_id": 6,
    "is_active": true
  }'
```

### Ejemplo 2: Cambio de Profesor en Turno

```bash
# ADMIN o el mismo JEFE_CARRERA puede actualizar el nombre
curl -X PATCH http://localhost:8000/degrees/2/jefe-carrera \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{
    "jefe_carrera": "Dr. Carlos Ramírez Soto"
  }'
```

### Ejemplo 3: Jefe de Carrera Consulta su Información

```bash
# 1. Login
curl -X POST http://localhost:8000/auth/login \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=jefe_sistemas&password=password123"

# 2. Obtener carrera asignada
curl -X GET http://localhost:8000/users/me/degree \
  -H "Authorization: Bearer <jefe_token>"
```

## Consideraciones de Rendimiento

- Los índices en `jefe_carrera_user_id` optimizan las consultas JOIN
- La relación uno-a-uno evita multiplicación de registros
- Los UNIQUE constraints previenen problemas de integridad

## Troubleshooting

### Error: "El usuario ya está asignado a otra carrera"

**Causa:** El usuario que intentas asignar ya tiene una carrera asignada.

**Solución:**
1. Verifica qué carrera tiene asignada:
```sql
SELECT * FROM degrees WHERE jefe_carrera_user_id = <user_id>;
```
2. Desasigna el usuario de la carrera actual:
```bash
PUT /degrees/<old_degree_id>/assign-user?user_id=<null>
```

### Error: "El usuario debe tener rol JEFE_CARRERA"

**Causa:** Intentas asignar un usuario que no tiene el rol correcto.

**Solución:**
1. Verifica el rol del usuario:
```bash
GET /users/
```
2. Cambia el rol si es necesario:
```bash
PUT /users/change-role?username=<username>&new_role=JEFE_CARRERA
```

## Referencias

- [API Documentation](./API.md) - Documentación completa de todos los endpoints
- [Degree Management](./DEGREES.md) - Guía detallada de gestión de carreras
- [Migrations](../migrations/README.md) - Historial y documentación de migraciones

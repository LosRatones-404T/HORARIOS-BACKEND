# Documentación de la API

Guía completa y navegable con descripción de endpoints, parámetros, cuerpos, respuestas, códigos HTTP y ejemplos funcionales.

Base URL local: `http://localhost:8000`

- OpenAPI/Swagger: `http://localhost:8000/docs`
- OpenAPI JSON: `http://localhost:8000/openapi.json`

---

## Autenticación

JWT basado en `Bearer`.

### POST `/auth/register`
Registra un nuevo usuario.

- Headers:
  - `Content-Type: application/json`
- Body (JSON):
```json
{
  "username": "juan",
  "email": "juan@example.com",
  "password": "MiPasswordSegura123",
  "role": "SECRETARIA",
  "degree_id": null
}
```
Para usuarios JEFE_CARRERA, incluye el ID de la carrera:
```json
{
  "username": "jefe1",
  "email": "jefe1@example.com",
  "password": "Password123",
  "role": "JEFE_CARRERA",
  "degree_id": 1
}
```
- Respuestas:
  - 201 Created:
```json
{
  "id": 1,
  "username": "juan",
  "email": "juan@example.com",
  "role": "SECRETARIA",
  "is_active": true,
  "degree_id": null,
  "degree": null
}
```
  - 400 Bad Request: datos inválidos
  - 409 Conflict: usuario ya existe

- Ejemplo curl:
```bash
curl -X POST http://localhost:8000/auth/register \
  -H "Content-Type: application/json" \
  -d '{"username":"juan","email":"juan@example.com","password":"MiPasswordSegura123","role":"SECRETARIA"}'
```

### POST `/auth/login`
Obtiene token de acceso.

- Headers:
  - `Content-Type: application/x-www-form-urlencoded`
- Body (form):
  - `username`: string
  - `password`: string
- Respuestas:
  - 200 OK:
```json
{ "access_token": "<jwt>", "token_type": "bearer" }
```
  - 401 Unauthorized: credenciales inválidas

- Ejemplo curl:
```bash
curl -X POST http://localhost:8000/auth/login \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=juan&password=MiPasswordSegura123"
```

### GET `/auth/me`
Perfil del usuario autenticado. Si el usuario es JEFE_CARRERA, incluye información de su carrera asociada.

- Headers:
  - `Authorization: Bearer <jwt>`
- Respuestas:
  - 200 OK (usuario regular):
```json
{
  "id": 1,
  "username": "juan",
  "email": "juan@example.com",
  "role": "SECRETARIA",
  "is_active": true,
  "degree_id": null,
  "degree": null
}
```
  - 200 OK (jefe de carrera):
```json
{
  "id": 2,
  "username": "jefe1",
  "email": "jefe1@example.com",
  "role": "JEFE_CARRERA",
  "is_active": true,
  "degree_id": 1,
  "degree": {
    "id": 1,
    "name": "Ingeniería en Sistemas Computacionales",
    "jefe_carrera": "Dr. Juan Pérez",
    "is_active": true
  }
}
```
  - 401 Unauthorized: token ausente/expirado

- Ejemplo curl:
```bash
curl http://localhost:8000/auth/me \
  -H "Authorization: Bearer <jwt>"
```

---

## Gestión de Usuarios

Endpoints para administrar usuarios y sus relaciones con carreras.

### GET `/users/`
Obtiene todos los usuarios del sistema.

- Headers:
  - `Authorization: Bearer <jwt>`
- Roles permitidos: Todos los usuarios autenticados
- Respuestas:
  - 200 OK:
```json
[
  {
    "id": 1,
    "username": "admin",
    "email": "admin@example.com",
    "role": "ADMIN",
    "is_active": true,
    "degree_id": null,
    "degree": null
  },
  {
    "id": 2,
    "username": "jefe1",
    "email": "jefe1@example.com",
    "role": "JEFE_CARRERA",
    "is_active": true,
    "degree_id": 1,
    "degree": {
      "id": 1,
      "name": "Ingeniería en Sistemas Computacionales",
      "jefe_carrera": "Dr. Juan Pérez",
      "is_active": true
    }
  }
]
```

- Ejemplo curl:
```bash
curl http://localhost:8000/users/ \
  -H "Authorization: Bearer <jwt>"
```

### GET `/users/jefes-carrera`
Obtiene todos los usuarios con rol JEFE_CARRERA.

- Headers:
  - `Authorization: Bearer <jwt>`
- Roles permitidos: Todos los usuarios autenticados
- Respuestas:
  - 200 OK: (lista de usuarios con role="JEFE_CARRERA")

- Ejemplo curl:
```bash
curl http://localhost:8000/users/jefes-carrera \
  -H "Authorization: Bearer <jwt>"
```

### GET `/users/by-degree/{degree_id}`
Obtiene todos los usuarios asociados a una carrera específica.

- Headers:
  - `Authorization: Bearer <jwt>`
- Roles permitidos: Todos los usuarios autenticados
- Parámetros:
  - `degree_id` (path): ID de la carrera
- Respuestas:
  - 200 OK: (lista de usuarios asociados a esa carrera)

- Ejemplo curl:
```bash
curl http://localhost:8000/users/by-degree/1 \
  -H "Authorization: Bearer <jwt>"
```

### PUT `/users/assign-degree`
Asigna una carrera a un usuario (especialmente útil para JEFE_CARRERA).

- Headers:
  - `Authorization: Bearer <jwt>`
  - `Content-Type: application/json`
- Roles permitidos: `ADMIN`
- Query Parameters:
  - `username` (query): Nombre de usuario
  - `degree_id` (query): ID de la carrera
- Respuestas:
  - 200 OK:
```json
{
  "id": 2,
  "username": "jefe1",
  "email": "jefe1@example.com",
  "role": "JEFE_CARRERA",
  "is_active": true,
  "degree_id": 1,
  "degree": {
    "id": 1,
    "name": "Ingeniería en Sistemas Computacionales",
    "jefe_carrera": "Dr. Juan Pérez",
    "is_active": true
  }
}
```
  - 403 Forbidden: rol insuficiente
  - 404 Not Found: usuario no encontrado

- Ejemplo curl:
```bash
curl -X PUT "http://localhost:8000/users/assign-degree?username=jefe1&degree_id=1" \
  -H "Authorization: Bearer <jwt>"
```

### PUT `/users/change-role`
Cambia el rol de un usuario.

- Headers:
  - `Authorization: Bearer <jwt>`
- Roles permitidos: Todos los usuarios autenticados
- Query Parameters:
  - `username` (query): Nombre de usuario
  - `new_role` (query): Nuevo rol
- Ejemplo curl:
```bash
curl -X PUT "http://localhost:8000/users/change-role?username=juan&new_role=JEFE_CARRERA" \
  -H "Authorization: Bearer <jwt>"
```

### POST `/users/update-password`
Actualiza la contraseña de un usuario.

- Headers:
  - `Authorization: Bearer <jwt>`
- Roles permitidos: Todos los usuarios autenticados
- Query Parameters:
  - `username` (query): Nombre de usuario
  - `new_password` (query): Nueva contraseña
- Ejemplo curl:
```bash
curl -X POST "http://localhost:8000/users/update-password?username=juan&new_password=NewPass123" \
  -H "Authorization: Bearer <jwt>"
```

### PUT `/users/toggle-active`
Cambia el estado activo/inactivo de un usuario.

- Headers:
  - `Authorization: Bearer <jwt>`
- Roles permitidos: Todos los usuarios autenticados
- Query Parameters:
  - `username` (query): Nombre de usuario
- Ejemplo curl:
```bash
curl -X PUT "http://localhost:8000/users/toggle-active?username=juan" \
  -H "Authorization: Bearer <jwt>"
```

### PUT `/users/change-email`
Cambia el email de un usuario.

- Headers:
  - `Authorization: Bearer <jwt>`
- Roles permitidos: Todos los usuarios autenticados
- Query Parameters:
  - `username` (query): Nombre de usuario
  - `new_email` (query): Nuevo email
- Ejemplo curl:
```bash
curl -X PUT "http://localhost:8000/users/change-email?username=juan&new_email=nuevo@example.com" \
  -H "Authorization: Bearer <jwt>"
```

---

## Exámenes

Endpoints para consultar y sembrar datos de exámenes.

### GET `/examenes/exams`
Lista de exámenes programados.

- Respuestas:
  - 200 OK:
```json
[
  {
    "id": 1,
    "course": "Diseño Estructurado de Algoritmos",
    "group": "106-A",
    "professor": "Mtro. Irving Ulises Hernández Miguel",
    "classroom": "CETI-S.O.",
    "date": "2025-10-28",
    "start": "17:00:00",
    "end": "19:00:00"
  }
]
```
  - 200 OK vacío: `[]`

- Ejemplo curl:
```bash
curl http://localhost:8000/examenes/exams
```

### POST `/examenes/seed-pdf-data`
Carga datos de ejemplo del PDF (grupo 106-A). Idempotente: si ya existen, avisa.

- Headers:
  - `Authorization: Bearer <jwt>` (si el proyecto exige auth para escribir; en esta versión puede estar abierto)
- Respuestas:
  - 200 OK:
```json
{ "message": "Datos del PDF (Grupo 106-A) cargados exitosamente" }
```
  - 200 OK (ya cargados):
```json
{ "message": "Los datos ya fueron cargados previamente." }
```

- Ejemplo curl:
```bash
curl -X POST http://localhost:8000/examenes/seed-pdf-data
```

---

## Códigos HTTP

- 200 OK: Operación exitosa.
- 201 Created: Recurso creado (registro de usuario).
- 400 Bad Request: Validación de entrada fallida.
- 401 Unauthorized: Autenticación requerida o inválida.
- 403 Forbidden: Autorización insuficiente (si se aplica control de roles).
- 404 Not Found: Recurso inexistente.
- 409 Conflict: Conflicto de recursos (usuario existente).
- 500 Internal Server Error: Error inesperado del servidor.

---

## Notas de uso

- Roles permitidos: `ADMIN`, `JEFE_CARRERA`, `JEFE_ESCOLARES`, `SECRETARIA`.
- El backend corre por defecto en `0.0.0.0:8000` (Docker) o `localhost:8000` local.
- Para consumir desde un frontend, asegúrate de configurar CORS si el origen es distinto.

---

## Ejemplos rápidos

Registrar, loguear y consultar perfil:
```bash
# Registro
curl -X POST http://localhost:8000/auth/register \
  -H "Content-Type: application/json" \
  -d '{"username":"demo","email":"demo@example.com","password":"Pass1234","role":"SECRETARIA"}'

# Login
TOKEN=(curl -s -X POST http://localhost:8000/auth/login \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=demo&password=Pass1234" | jq -r .access_token)

# Perfil
curl http://localhost:8000/auth/me -H "Authorization: Bearer $TOKEN"
```

Listar exámenes y sembrar datos:
```bash
curl http://localhost:8000/examenes/exams
curl -X POST http://localhost:8000/examenes/seed-pdf-data
```

---

## Carreras (Degrees)

Endpoints para gestionar las carreras y sus jefes de carrera en turno.

### GET `/degrees/`
Lista todas las carreras.

- Headers:
  - `Authorization: Bearer <jwt>`
- Roles permitidos: `ADMIN`, `JEFE_CARRERA`, `JEFE_ESCOLARES`, `SECRETARIA`
- Respuestas:
  - 200 OK:
```json
[
  {
    "id": 1,
    "name": "Ingeniería en Sistemas Computacionales",
    "jefe_carrera": "Dr. Juan Pérez",
    "is_active": true
  },
  {
    "id": 2,
    "name": "Ingeniería Industrial",
    "jefe_carrera": "Mtro. Carlos López",
    "is_active": true
  }
]
```
  - 401 Unauthorized: token ausente/expirado

- Ejemplo curl:
```bash
curl http://localhost:8000/degrees/ \
  -H "Authorization: Bearer <jwt>"
```

### GET `/degrees/active`
Lista solo las carreras activas.

- Headers:
  - `Authorization: Bearer <jwt>`
- Roles permitidos: `ADMIN`, `JEFE_CARRERA`, `JEFE_ESCOLARES`, `SECRETARIA`
- Respuestas:
  - 200 OK: (mismo formato que `/degrees/`)
  - 401 Unauthorized: token ausente/expirado

- Ejemplo curl:
```bash
curl http://localhost:8000/degrees/active \
  -H "Authorization: Bearer <jwt>"
```

### GET `/degrees/{degree_id}`
Obtiene una carrera específica por ID.

- Headers:
  - `Authorization: Bearer <jwt>`
- Roles permitidos: `ADMIN`, `JEFE_CARRERA`, `JEFE_ESCOLARES`, `SECRETARIA`
- Parámetros:
  - `degree_id` (path): ID de la carrera
- Respuestas:
  - 200 OK:
```json
{
  "id": 1,
  "name": "Ingeniería en Sistemas Computacionales",
  "jefe_carrera": "Dr. Juan Pérez",
  "is_active": true
}
```
  - 404 Not Found: carrera no encontrada
  - 401 Unauthorized: token ausente/expirado

- Ejemplo curl:
```bash
curl http://localhost:8000/degrees/1 \
  -H "Authorization: Bearer <jwt>"
```

### POST `/degrees/`
Crea una nueva carrera.

- Headers:
  - `Authorization: Bearer <jwt>`
  - `Content-Type: application/json`
- Roles permitidos: `ADMIN`
- Body (JSON):
```json
{
  "name": "Ingeniería en Mecatrónica",
  "jefe_carrera": "Dra. María González",
  "is_active": true
}
```
- Respuestas:
  - 201 Created:
```json
{
  "id": 3,
  "name": "Ingeniería en Mecatrónica",
  "jefe_carrera": "Dra. María González",
  "is_active": true
}
```
  - 400 Bad Request: nombre duplicado o datos inválidos
  - 403 Forbidden: rol insuficiente
  - 401 Unauthorized: token ausente/expirado

- Ejemplo curl:
```bash
curl -X POST http://localhost:8000/degrees/ \
  -H "Authorization: Bearer <jwt>" \
  -H "Content-Type: application/json" \
  -d '{"name":"Ingeniería en Mecatrónica","jefe_carrera":"Dra. María González","is_active":true}'
```

### PATCH `/degrees/{degree_id}/jefe-carrera`
**Actualiza solo el jefe de carrera en turno.**

Este es el endpoint principal para tu requerimiento: permite cambiar qué profesor está actualmente como jefe de carrera, sin afectar los usuarios con rol `JEFE_CARRERA` del sistema.

- Headers:
  - `Authorization: Bearer <jwt>`
  - `Content-Type: application/json`
- Roles permitidos: `ADMIN`, `JEFE_CARRERA`
- Parámetros:
  - `degree_id` (path): ID de la carrera
- Body (JSON):
```json
{
  "jefe_carrera": "Mtro. Roberto Sánchez"
}
```
- Respuestas:
  - 200 OK:
```json
{
  "id": 1,
  "name": "Ingeniería en Sistemas Computacionales",
  "jefe_carrera": "Mtro. Roberto Sánchez",
  "is_active": true
}
```
  - 404 Not Found: carrera no encontrada
  - 403 Forbidden: rol insuficiente
  - 401 Unauthorized: token ausente/expirado

- Ejemplo curl:
```bash
curl -X PATCH http://localhost:8000/degrees/1/jefe-carrera \
  -H "Authorization: Bearer <jwt>" \
  -H "Content-Type: application/json" \
  -d '{"jefe_carrera":"Mtro. Roberto Sánchez"}'
```

### PUT `/degrees/{degree_id}`
Actualiza una carrera completa.

- Headers:
  - `Authorization: Bearer <jwt>`
  - `Content-Type: application/json`
- Roles permitidos: `ADMIN`
- Parámetros:
  - `degree_id` (path): ID de la carrera
- Body (JSON) - Todos los campos son opcionales:
```json
{
  "name": "Ingeniería en Sistemas Computacionales y Redes",
  "jefe_carrera": "Dr. Juan Pérez López",
  "is_active": false
}
```
- Respuestas:
  - 200 OK:
```json
{
  "id": 1,
  "name": "Ingeniería en Sistemas Computacionales y Redes",
  "jefe_carrera": "Dr. Juan Pérez López",
  "is_active": false
}
```
  - 400 Bad Request: nombre duplicado o datos inválidos
  - 403 Forbidden: rol insuficiente
  - 401 Unauthorized: token ausente/expirado

- Ejemplo curl:
```bash
curl -X PUT http://localhost:8000/degrees/1 \
  -H "Authorization: Bearer <jwt>" \
  -H "Content-Type: application/json" \
  -d '{"name":"Ingeniería en Sistemas Computacionales y Redes","jefe_carrera":"Dr. Juan Pérez López"}'
```

### PATCH `/degrees/{degree_id}/toggle-status`
Cambia el estado activo/inactivo de una carrera.

- Headers:
  - `Authorization: Bearer <jwt>`
- Roles permitidos: `ADMIN`
- Parámetros:
  - `degree_id` (path): ID de la carrera
- Respuestas:
  - 200 OK:
```json
{
  "id": 1,
  "name": "Ingeniería en Sistemas Computacionales",
  "jefe_carrera": "Dr. Juan Pérez",
  "is_active": false
}
```
  - 404 Not Found: carrera no encontrada
  - 403 Forbidden: rol insuficiente
  - 401 Unauthorized: token ausente/expirado

- Ejemplo curl:
```bash
curl -X PATCH http://localhost:8000/degrees/1/toggle-status \
  -H "Authorization: Bearer <jwt>"
```

### DELETE `/degrees/{degree_id}`
Elimina una carrera.

- Headers:
  - `Authorization: Bearer <jwt>`
- Roles permitidos: `ADMIN`
- Parámetros:
  - `degree_id` (path): ID de la carrera
- Respuestas:
  - 200 OK:
```json
{
  "message": "Carrera eliminada exitosamente"
}
```
  - 404 Not Found: carrera no encontrada
  - 403 Forbidden: rol insuficiente
  - 401 Unauthorized: token ausente/expirado

- Ejemplo curl:
```bash
curl -X DELETE http://localhost:8000/degrees/1 \
  -H "Authorization: Bearer <jwt>"
```

# Cambio de degree_id a tipo String

## Fecha: 21 de enero de 2026

## Motivo
El usuario solicitó que `degree_id` sea de tipo `str` en lugar de `INTEGER` para permitir IDs alfanuméricos como "ISC", "IE", "IM", etc.

## Archivos Modificados

### 1. Modelo de Base de Datos
**Archivo:** `app/models/models.py`
- Cambió `id = Column(Integer, ...)` a `id = Column(String, ...)`

### 2. Schemas (Validación)
**Archivo:** `app/schemas/degree_schemas.py`
- `DegreeRead.id`: Cambió de `int` a `str`
- `DegreeCreate`: Agregó campo `id: str` obligatorio

### 3. Repository (Acceso a Datos)
**Archivo:** `app/repositories/degree_repository.py`
- `get_degree_by_id(degree_id: str)` - antes `int`
- `create_degree(id: str, ...)` - agregó parámetro `id`
- `update_degree_jefe_carrera(degree_id: str, ...)` - antes `int`
- `update_degree(degree_id: str, ...)` - antes `int`
- `assign_jefe_carrera_user(degree_id: str, ...)` - antes `int`
- `toggle_degree_status(degree_id: str)` - antes `int`
- `delete_degree(degree_id: str)` - antes `int`

### 4. Service (Lógica de Negocio)
**Archivo:** `app/services/degree_service.py`
- `get_degree_by_id(degree_id: str)` - antes `int`
- `create_degree(...)` - ahora pasa `id=degree_data.id` al repository
- `update_jefe_carrera(degree_id: str, ...)` - antes `int`
- `update_degree(degree_id: str, ...)` - antes `int`
- `assign_jefe_carrera_user(degree_id: str, ...)` - antes `int`
- `toggle_degree_status(degree_id: str)` - antes `int`
- `delete_degree(degree_id: str)` - antes `int`

### 5. API Routes (Endpoints)
**Archivo:** `app/api/degree_routes.py`
- `GET /{degree_id}` - parámetro cambió de `int` a `str`
- `PATCH /{degree_id}/jefe-carrera` - parámetro cambió de `int` a `str`
- `PUT /{degree_id}/assign-user` - parámetro cambió de `int` a `str`
- `PUT /{degree_id}` - parámetro cambió de `int` a `str`
- `PATCH /{degree_id}/toggle-status` - parámetro cambió de `int` a `str`
- `DELETE /{degree_id}` - parámetro cambió de `int` a `str`

### 6. Migración de Base de Datos
**Archivos creados:**
- `migrations/003_change_degree_id_to_varchar.sql`
- `migrations/003_change_degree_id_to_varchar.py`

**Proceso de migración:**
1. Crear columna temporal `id_new VARCHAR`
2. Copiar datos de `id` (INTEGER) a `id_new` (VARCHAR)
3. Eliminar constraint PRIMARY KEY
4. Eliminar columna `id`
5. Renombrar `id_new` a `id`
6. Establecer NOT NULL
7. Crear nuevo PRIMARY KEY
8. Recrear índice

## Uso del Nuevo Sistema

### Crear Carrera
Antes:
```json
POST /degrees/
{
  "name": "Ingeniería en Sistemas",
  "jefe_carrera": "Dr. Juan Pérez"
}
```

Ahora:
```json
POST /degrees/
{
  "id": "ISC",
  "name": "Ingeniería en Sistemas Computacionales",
  "jefe_carrera": "Dr. Juan Pérez"
}
```

### Obtener Carrera por ID
Antes:
```bash
GET /degrees/1
```

Ahora:
```bash
GET /degrees/ISC
```

### Actualizar Carrera
Antes:
```bash
PUT /degrees/1
```

Ahora:
```bash
PUT /degrees/ISC
```

## Ejemplos de IDs Válidos

- "ISC" - Ingeniería en Sistemas Computacionales
- "IE" - Ingeniería Electrónica
- "IM" - Ingeniería Mecánica
- "IQ" - Ingeniería Química
- "LA" - Licenciatura en Administración
- "LC" - Licenciatura en Contaduría

## Ventajas del Cambio

1. **IDs Semánticos:** Los IDs son legibles y tienen significado ("ISC" vs "1")
2. **Compatibilidad:** Permite sincronizar con sistemas externos que usan códigos de carrera
3. **URLs Amigables:** `/degrees/ISC` es más claro que `/degrees/1`
4. **Flexibilidad:** Permite IDs alfanuméricos establecidos por la institución

## Consideraciones

1. **Unicidad:** Los IDs deben ser únicos (constraint PRIMARY KEY)
2. **Formato:** Se recomienda usar mayúsculas y sin espacios
3. **Longitud:** Mantener IDs cortos (2-5 caracteres) para facilidad de uso
4. **Inmutabilidad:** Una vez creado, el ID no debería cambiar

## Migración de Datos Existentes

Si existen datos con IDs INTEGER, la migración los convertirá a VARCHAR:
- `1` → `"1"`
- `2` → `"2"`
- etc.

Se recomienda actualizar manualmente a IDs semánticos:
```sql
UPDATE degrees SET id = 'ISC' WHERE id = '1';
UPDATE degrees SET id = 'IE' WHERE id = '2';
-- etc.
```

## Rollback

Si es necesario revertir a INTEGER:
```bash
python migrations/003_change_degree_id_to_varchar.py --rollback
```

**Nota:** El rollback solo funciona si todos los valores en `id` son numéricos.

## Testing

Después de aplicar los cambios, probar:

1. **Crear carrera con ID string:**
```bash
POST /degrees/
{
  "id": "TEST",
  "name": "Carrera de Prueba",
  "is_active": true
}
```

2. **Obtener por ID string:**
```bash
GET /degrees/TEST
```

3. **Actualizar:**
```bash
PUT /degrees/TEST
{
  "name": "Carrera de Prueba Actualizada"
}
```

4. **Eliminar:**
```bash
DELETE /degrees/TEST
```

## Estado de la Migración

- ✅ Código actualizado (modelos, schemas, repositories, services, routes)
- ✅ Scripts de migración creados (SQL y Python)
- ⏳ Migración pendiente de ejecutar en base de datos
- ⏳ Testing pendiente

## Próximos Pasos

1. Ejecutar migración SQL:
```bash
docker exec -i postgres-horarios psql -U user_horarios -d horarios_db < migrations/003_change_degree_id_to_varchar.sql
```

2. Verificar estructura:
```bash
docker exec postgres-horarios psql -U user_horarios -d horarios_db -c "\d degrees"
```

3. Actualizar datos existentes a IDs semánticos

4. Probar todos los endpoints con IDs string

5. Actualizar documentación de API

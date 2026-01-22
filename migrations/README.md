# Database Migrations

Este directorio contiene las migraciones de base de datos para el proyecto HORARIOS-BACKEND.

## Migraciones Disponibles

### 001_add_degree_id_to_users.sql
**Fecha:** 2024  
**Estado:** ⚠️ Revertida por migración 002  
**Descripción:** Agregó columna `degree_id` a la tabla `users` para establecer relación User → Degree (muchos a uno).

**Cambios realizados:**
- Agregó columna `degree_id INTEGER` a tabla `users`
- Creó foreign key `users_degree_id_fkey` (users.degree_id → degrees.id)
- Creó índice `ix_users_degree_id`
- ON DELETE SET NULL para mantener usuarios si se elimina la carrera

**Nota:** Esta migración fue revertida porque se cambió el diseño a una relación Degree → User (uno a uno).

---

### 002_reverse_user_degree_relationship.sql
**Fecha:** 2024  
**Estado:** ✅ Aplicada  
**Descripción:** Revirtió la relación User-Degree para establecer una relación Degree → User (uno a uno).

**Cambios realizados:**
1. **Eliminó de `users`:**
   - Constraint `users_degree_id_fkey`
   - Índice `ix_users_degree_id`
   - Columna `degree_id`

2. **Agregó a `degrees`:**
   - Columna `jefe_carrera_user_id INTEGER`
   - Constraint UNIQUE `degrees_jefe_carrera_user_id_unique`
   - Foreign key `degrees_jefe_carrera_user_id_fkey` (degrees.jefe_carrera_user_id → users.id)
   - Índice `ix_degrees_jefe_carrera_user_id`

**Razón del cambio:**
- Cada carrera debe tener exactamente UN usuario JEFE_CARRERA asignado
- Un usuario solo puede ser jefe de UNA carrera
- Separar el concepto de "usuario del sistema" (jefe_carrera_user_id) del "profesor en turno" (jefe_carrera)

## Cómo Ejecutar Migraciones

### Método 1: Docker + psql (Recomendado)

```bash
# Ejecutar migración SQL directamente
docker exec -i postgres-horarios psql -U user_horarios -d horarios_db < migrations/002_reverse_user_degree_relationship.sql
```

### Método 2: Script Python (Requiere dependencias)

```bash
# Asegúrate de tener las dependencias instaladas
pip install sqlalchemy psycopg2-binary

# Ejecutar migración
python migrations/002_reverse_user_degree_relationship.py

# Rollback (revertir)
python migrations/002_reverse_user_degree_relationship.py --rollback
```

### Método 3: Desde psql directamente

```bash
# Conectarse al contenedor
docker exec -it postgres-horarios psql -U user_horarios -d horarios_db

# Ejecutar comandos SQL manualmente
\i /path/to/migrations/002_reverse_user_degree_relationship.sql
```

## Verificar Estado de Migraciones

```bash
# Ver estructura de tabla users
docker exec -it postgres-horarios psql -U user_horarios -d horarios_db -c "\d users"

# Ver estructura de tabla degrees
docker exec -it postgres-horarios psql -U user_horarios -d horarios_db -c "\d degrees"

# Ver todas las foreign keys
docker exec -it postgres-horarios psql -U user_horarios -d horarios_db -c "
SELECT
    tc.table_name,
    kcu.column_name,
    ccu.table_name AS foreign_table_name,
    ccu.column_name AS foreign_column_name
FROM information_schema.table_constraints AS tc
JOIN information_schema.key_column_usage AS kcu
    ON tc.constraint_name = kcu.constraint_name
JOIN information_schema.constraint_column_usage AS ccu
    ON ccu.constraint_name = tc.constraint_name
WHERE tc.constraint_type = 'FOREIGN KEY'
    AND tc.table_name IN ('users', 'degrees');
"
```

## Crear Nueva Migración

1. **Crear archivo SQL:**
```bash
touch migrations/003_nombre_descriptivo.sql
```

2. **Escribir comandos SQL:**
```sql
-- Migration: 003_nombre_descriptivo.sql
-- Description: Descripción de los cambios

-- Tus comandos SQL aquí
ALTER TABLE ...;
```

3. **Crear script Python (opcional):**
```python
# migrations/003_nombre_descriptivo.py
# Seguir el patrón de 002_reverse_user_degree_relationship.py
```

4. **Ejecutar:**
```bash
docker exec -i postgres-horarios psql -U user_horarios -d horarios_db < migrations/003_nombre_descriptivo.sql
```

5. **Actualizar este README:**
```markdown
### 003_nombre_descriptivo.sql
**Fecha:** 2024  
**Estado:** ✅ Aplicada  
**Descripción:** ...
```

## Rollback de Migraciones

### Rollback de Migración 002

**Usando script Python:**
```bash
python migrations/002_reverse_user_degree_relationship.py --rollback
```

**Usando SQL manual:**
```sql
-- Revertir cambios manualmente
ALTER TABLE degrees DROP CONSTRAINT IF EXISTS degrees_jefe_carrera_user_id_fkey;
ALTER TABLE degrees DROP CONSTRAINT IF EXISTS degrees_jefe_carrera_user_id_unique;
DROP INDEX IF EXISTS ix_degrees_jefe_carrera_user_id;
ALTER TABLE degrees DROP COLUMN IF EXISTS jefe_carrera_user_id;

-- Restaurar esquema anterior
ALTER TABLE users ADD COLUMN IF NOT EXISTS degree_id INTEGER;
ALTER TABLE users ADD CONSTRAINT users_degree_id_fkey 
    FOREIGN KEY (degree_id) REFERENCES degrees(id) ON DELETE SET NULL;
CREATE INDEX IF NOT EXISTS ix_users_degree_id ON users(degree_id);
```

## Mejores Prácticas

1. **Siempre hacer backup antes de migrar:**
```bash
docker exec postgres-horarios pg_dump -U user_horarios horarios_db > backup_$(date +%Y%m%d_%H%M%S).sql
```

2. **Probar en entorno de desarrollo primero**

3. **Documentar cada migración** en este README

4. **Usar transacciones** (BEGIN/COMMIT) cuando sea posible

5. **Incluir scripts de rollback** para cada migración

6. **Verificar constraints** después de migrar:
```bash
docker exec -it postgres-horarios psql -U user_horarios -d horarios_db -c "\d+ tablename"
```

## Estado Actual del Schema

### Tabla `users`
```sql
- id (INTEGER, PK)
- username (VARCHAR, UNIQUE)
- email (VARCHAR, UNIQUE)
- hashed_password (VARCHAR)
- role (VARCHAR)
- is_active (BOOLEAN)
- created_at (TIMESTAMP)
```

### Tabla `degrees`
```sql
- id (INTEGER, PK)
- name (VARCHAR, UNIQUE)
- jefe_carrera (VARCHAR)
- jefe_carrera_user_id (INTEGER, UNIQUE, FK → users.id)
- is_active (BOOLEAN)
- created_at (TIMESTAMP)
```

### Relaciones
- `degrees.jefe_carrera_user_id` → `users.id` (uno a uno, UNIQUE)
- ON DELETE SET NULL (si se elimina el usuario, el campo se pone en NULL)

## Troubleshooting

### Error: "relation does not exist"
**Causa:** La tabla no existe en la base de datos.  
**Solución:** Verificar que la base de datos esté inicializada. Ejecutar script de inicialización si es necesario.

### Error: "column already exists"
**Causa:** La migración ya fue aplicada.  
**Solución:** Verificar el estado actual con `\d tablename` y ajustar la migración.

### Error: "constraint already exists"
**Causa:** El constraint ya existe en la base de datos.  
**Solución:** Usar `DROP CONSTRAINT IF EXISTS` antes de crear.

## Referencias

- [PostgreSQL ALTER TABLE](https://www.postgresql.org/docs/current/sql-altertable.html)
- [SQLAlchemy Migrations](https://alembic.sqlalchemy.org/en/latest/)
- [Database Design Best Practices](https://www.postgresql.org/docs/current/ddl.html)

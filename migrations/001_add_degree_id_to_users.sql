-- Migración: Agregar columna degree_id y relación con degrees a la tabla users
-- Fecha: 2026-01-21

BEGIN;

-- Agregar columna degree_id a la tabla users
ALTER TABLE users 
ADD COLUMN degree_id INTEGER;

-- Agregar constraint de foreign key
ALTER TABLE users 
ADD CONSTRAINT users_degree_id_fkey 
FOREIGN KEY (degree_id) REFERENCES degrees(id);

-- Agregar índice para mejorar el rendimiento de las consultas
CREATE INDEX ix_users_degree_id ON users(degree_id);

COMMIT;

-- Verificar que la columna se agregó correctamente
SELECT column_name, data_type, is_nullable 
FROM information_schema.columns 
WHERE table_name = 'users' AND column_name = 'degree_id';

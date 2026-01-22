#!/bin/bash

echo "=== Verificando estructura de la tabla degrees ==="
docker exec postgres-horarios psql -U user_horarios -d horarios_db -t -c "
SELECT 
    column_name, 
    data_type, 
    is_nullable,
    column_default
FROM information_schema.columns 
WHERE table_name='degrees' 
ORDER BY ordinal_position;
"

echo ""
echo "=== Verificando constraints de degrees ==="
docker exec postgres-horarios psql -U user_horarios -d horarios_db -t -c "
SELECT 
    tc.constraint_name,
    tc.constraint_type,
    kcu.column_name
FROM information_schema.table_constraints tc
JOIN information_schema.key_column_usage kcu 
    ON tc.constraint_name = kcu.constraint_name
WHERE tc.table_name = 'degrees'
ORDER BY tc.constraint_type;
"

echo ""
echo "=== Verificando estructura de la tabla users ==="
docker exec postgres-horarios psql -U user_horarios -d horarios_db -t -c "
SELECT 
    column_name, 
    data_type, 
    is_nullable
FROM information_schema.columns 
WHERE table_name='users' 
ORDER BY ordinal_position;
"

echo ""
echo "=== Verificando foreign keys ==="
docker exec postgres-horarios psql -U user_horarios -d horarios_db -t -c "
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
    AND tc.table_name IN ('users', 'degrees')
ORDER BY tc.table_name;
"

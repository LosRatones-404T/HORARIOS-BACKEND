BEGIN;

-- Verificar el tipo actual
DO $$
BEGIN
    IF EXISTS (
        SELECT 1 FROM information_schema.columns 
        WHERE table_name = 'degrees' AND column_name = 'id' AND data_type = 'integer'
    ) THEN
        -- Crear columna temporal
        ALTER TABLE degrees ADD COLUMN id_temp VARCHAR;
        
        -- Copiar datos
        UPDATE degrees SET id_temp = id::VARCHAR;
        
        -- Eliminar primary key
        ALTER TABLE degrees DROP CONSTRAINT IF EXISTS degrees_pkey;
        
        -- Eliminar columna vieja
        ALTER TABLE degrees DROP COLUMN id;
        
        -- Renombrar columna
        ALTER TABLE degrees RENAME COLUMN id_temp TO id;
        
        -- Establecer NOT NULL
        ALTER TABLE degrees ALTER COLUMN id SET NOT NULL;
        
        -- Crear primary key
        ALTER TABLE degrees ADD PRIMARY KEY (id);
        
        -- Crear índice
        CREATE INDEX IF NOT EXISTS ix_degrees_id ON degrees(id);
        
        RAISE NOTICE 'Migration completed: degrees.id is now VARCHAR';
    ELSE
        RAISE NOTICE 'degrees.id is already VARCHAR, skipping migration';
    END IF;
END $$;

COMMIT;

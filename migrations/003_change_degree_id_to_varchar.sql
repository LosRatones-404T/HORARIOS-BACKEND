-- Migration: 003_change_degree_id_to_varchar.sql
-- Description: Change degrees.id from INTEGER to VARCHAR
-- Note: This is a potentially breaking change. Ensure no foreign keys reference degrees.id
--       or update them accordingly.

-- Step 1: Check if there are any foreign keys referencing degrees.id
-- (This is informational - uncomment to check before running)
-- SELECT
--     tc.constraint_name, 
--     tc.table_name, 
--     kcu.column_name
-- FROM information_schema.table_constraints AS tc 
-- JOIN information_schema.key_column_usage AS kcu
--     ON tc.constraint_name = kcu.constraint_name
-- WHERE tc.constraint_type = 'FOREIGN KEY' 
--     AND kcu.referenced_table_name = 'degrees';

-- Step 2: Create a new temporary column with VARCHAR type
ALTER TABLE degrees ADD COLUMN id_new VARCHAR;

-- Step 3: Copy data from old id to new id_new (converting INTEGER to VARCHAR)
UPDATE degrees SET id_new = id::VARCHAR;

-- Step 4: Drop the old primary key constraint
ALTER TABLE degrees DROP CONSTRAINT IF EXISTS degrees_pkey;

-- Step 5: Drop the old id column
ALTER TABLE degrees DROP COLUMN id;

-- Step 6: Rename id_new to id
ALTER TABLE degrees RENAME COLUMN id_new TO id;

-- Step 7: Set id as NOT NULL
ALTER TABLE degrees ALTER COLUMN id SET NOT NULL;

-- Step 8: Create new primary key constraint
ALTER TABLE degrees ADD PRIMARY KEY (id);

-- Step 9: Recreate the index
CREATE INDEX IF NOT EXISTS ix_degrees_id ON degrees(id);

-- Verification query (uncomment to check)
-- SELECT column_name, data_type, is_nullable 
-- FROM information_schema.columns 
-- WHERE table_name = 'degrees' AND column_name = 'id';

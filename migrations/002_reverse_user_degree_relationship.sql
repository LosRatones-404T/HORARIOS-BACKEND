-- Migration: 002_reverse_user_degree_relationship.sql
-- Description: Reverse the User-Degree relationship
-- Changes:
--   1. Remove degree_id from users table
--   2. Add jefe_carrera_user_id to degrees table with UNIQUE constraint
--   3. Create foreign key from degrees to users

-- Step 1: Remove the foreign key constraint and column from users table
ALTER TABLE users DROP CONSTRAINT IF EXISTS users_degree_id_fkey;
DROP INDEX IF EXISTS ix_users_degree_id;
ALTER TABLE users DROP COLUMN IF EXISTS degree_id;

-- Step 2: Change degrees.id type to VARCHAR and add jefe_carrera_user_id column
-- Note: If degrees.id needs to be changed from INTEGER to VARCHAR, this requires more complex migration
-- For now, we assume degrees.id is already VARCHAR or will be migrated separately
ALTER TABLE degrees ADD COLUMN IF NOT EXISTS jefe_carrera_user_id INTEGER;

-- Step 3: Create UNIQUE constraint (ensures one user per degree)
ALTER TABLE degrees ADD CONSTRAINT degrees_jefe_carrera_user_id_unique UNIQUE (jefe_carrera_user_id);

-- Step 4: Create foreign key constraint
ALTER TABLE degrees 
ADD CONSTRAINT degrees_jefe_carrera_user_id_fkey 
FOREIGN KEY (jefe_carrera_user_id) 
REFERENCES users(id) 
ON DELETE SET NULL;

-- Step 5: Create index for performance
CREATE INDEX IF NOT EXISTS ix_degrees_jefe_carrera_user_id ON degrees(jefe_carrera_user_id);

-- Verification query (uncomment to check)
-- SELECT column_name, data_type, is_nullable 
-- FROM information_schema.columns 
-- WHERE table_name IN ('users', 'degrees') 
-- ORDER BY table_name, ordinal_position;

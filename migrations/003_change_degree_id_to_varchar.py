#!/usr/bin/env python3
"""
Migration Script: 003_change_degree_id_to_varchar.py
Description: Change degrees.id from INTEGER to VARCHAR
"""

import os
import sys
from pathlib import Path

# Add parent directory to path to import app modules
sys.path.append(str(Path(__file__).parent.parent))

from sqlalchemy import create_engine, text
from app.core.config import settings

def run_migration():
    """Execute the migration"""
    DATABASE_URL = f"postgresql://{settings.POSTGRES_USER}:{settings.POSTGRES_PASSWORD}@{settings.POSTGRES_SERVER}:{settings.POSTGRES_PORT}/{settings.POSTGRES_DB}"
    engine = create_engine(DATABASE_URL)
    
    print(f"Connecting to database: {settings.POSTGRES_DB}")
    print("Starting migration 003: Change degrees.id to VARCHAR...")
    
    try:
        with engine.begin() as connection:
            # Step 1: Check for foreign keys (informational)
            print("Step 1: Checking for foreign keys referencing degrees.id...")
            result = connection.execute(text("""
                SELECT
                    tc.constraint_name, 
                    tc.table_name, 
                    kcu.column_name
                FROM information_schema.table_constraints AS tc 
                JOIN information_schema.key_column_usage AS kcu
                    ON tc.constraint_name = kcu.constraint_name
                WHERE tc.constraint_type = 'FOREIGN KEY' 
                    AND ccu.table_name = 'degrees'
                    AND ccu.column_name = 'id'
                FROM information_schema.constraint_column_usage AS ccu
                WHERE ccu.constraint_name = tc.constraint_name;
            """))
            fks = result.fetchall()
            if fks:
                print(f"  ⚠️  Warning: Found {len(fks)} foreign keys referencing degrees.id")
                for fk in fks:
                    print(f"    - {fk[1]}.{fk[2]} ({fk[0]})")
            else:
                print("  ✓ No foreign keys found")
            
            # Step 2: Create temporary column
            print("Step 2: Creating temporary VARCHAR column...")
            connection.execute(text("""
                ALTER TABLE degrees ADD COLUMN id_new VARCHAR;
            """))
            print("  ✓ Created id_new column")
            
            # Step 3: Copy data
            print("Step 3: Copying data from id to id_new...")
            connection.execute(text("""
                UPDATE degrees SET id_new = id::VARCHAR;
            """))
            print("  ✓ Data copied")
            
            # Step 4: Drop old primary key
            print("Step 4: Dropping old primary key constraint...")
            connection.execute(text("""
                ALTER TABLE degrees DROP CONSTRAINT IF EXISTS degrees_pkey;
            """))
            print("  ✓ Primary key dropped")
            
            # Step 5: Drop old id column
            print("Step 5: Dropping old id column...")
            connection.execute(text("""
                ALTER TABLE degrees DROP COLUMN id;
            """))
            print("  ✓ Old id column dropped")
            
            # Step 6: Rename id_new to id
            print("Step 6: Renaming id_new to id...")
            connection.execute(text("""
                ALTER TABLE degrees RENAME COLUMN id_new TO id;
            """))
            print("  ✓ Column renamed")
            
            # Step 7: Set NOT NULL
            print("Step 7: Setting id as NOT NULL...")
            connection.execute(text("""
                ALTER TABLE degrees ALTER COLUMN id SET NOT NULL;
            """))
            print("  ✓ NOT NULL constraint added")
            
            # Step 8: Create new primary key
            print("Step 8: Creating new primary key constraint...")
            connection.execute(text("""
                ALTER TABLE degrees ADD PRIMARY KEY (id);
            """))
            print("  ✓ Primary key created")
            
            # Step 9: Recreate index
            print("Step 9: Recreating index...")
            connection.execute(text("""
                CREATE INDEX IF NOT EXISTS ix_degrees_id ON degrees(id);
            """))
            print("  ✓ Index created")
            
        print("\n✅ Migration 003 completed successfully!")
        print("\nNew schema:")
        print("  - degrees.id is now VARCHAR instead of INTEGER")
        print("  - All constraints and indexes recreated")
        
    except Exception as e:
        print(f"\n❌ Migration failed: {e}")
        print("\nNote: If the migration failed partway through, you may need to:")
        print("  1. Check the current state of the degrees table")
        print("  2. Manually fix any issues")
        print("  3. Use the rollback script if necessary")
        raise

def rollback_migration():
    """Rollback the migration (restore to INTEGER)"""
    DATABASE_URL = f"postgresql://{settings.POSTGRES_USER}:{settings.POSTGRES_PASSWORD}@{settings.POSTGRES_SERVER}:{settings.POSTGRES_PORT}/{settings.POSTGRES_DB}"
    engine = create_engine(DATABASE_URL)
    
    print(f"Connecting to database: {settings.POSTGRES_DB}")
    print("Rolling back migration 003...")
    
    try:
        with engine.begin() as connection:
            # Create temporary INTEGER column
            print("Step 1: Creating temporary INTEGER column...")
            connection.execute(text("""
                ALTER TABLE degrees ADD COLUMN id_new INTEGER;
            """))
            
            # Copy data (VARCHAR to INTEGER - this will fail if any non-numeric values exist)
            print("Step 2: Converting VARCHAR to INTEGER...")
            connection.execute(text("""
                UPDATE degrees SET id_new = id::INTEGER;
            """))
            
            # Drop old primary key
            print("Step 3: Dropping current primary key...")
            connection.execute(text("""
                ALTER TABLE degrees DROP CONSTRAINT IF EXISTS degrees_pkey;
            """))
            
            # Drop VARCHAR id column
            print("Step 4: Dropping VARCHAR id column...")
            connection.execute(text("""
                ALTER TABLE degrees DROP COLUMN id;
            """))
            
            # Rename id_new to id
            print("Step 5: Renaming id_new to id...")
            connection.execute(text("""
                ALTER TABLE degrees RENAME COLUMN id_new TO id;
            """))
            
            # Set NOT NULL
            print("Step 6: Setting NOT NULL constraint...")
            connection.execute(text("""
                ALTER TABLE degrees ALTER COLUMN id SET NOT NULL;
            """))
            
            # Create primary key
            print("Step 7: Creating primary key...")
            connection.execute(text("""
                ALTER TABLE degrees ADD PRIMARY KEY (id);
            """))
            
            # Recreate index
            print("Step 8: Recreating index...")
            connection.execute(text("""
                CREATE INDEX IF NOT EXISTS ix_degrees_id ON degrees(id);
            """))
            
        print("\n✅ Rollback completed successfully!")
        print("\nRestored schema:")
        print("  - degrees.id is back to INTEGER")
        
    except Exception as e:
        print(f"\n❌ Rollback failed: {e}")
        print("\nNote: Rollback may fail if:")
        print("  - VARCHAR values cannot be converted to INTEGER")
        print("  - You may need to manually clean the data first")
        raise

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Migration 003: Change degrees.id to VARCHAR")
    parser.add_argument("--rollback", action="store_true", help="Rollback the migration")
    
    args = parser.parse_args()
    
    if args.rollback:
        rollback_migration()
    else:
        run_migration()

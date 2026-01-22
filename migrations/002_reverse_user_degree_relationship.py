#!/usr/bin/env python3
"""
Migration Script: 002_reverse_user_degree_relationship.py
Description: Reverse the User-Degree relationship from User->Degree to Degree->User
"""

import os
import sys
from pathlib import Path

# Add parent directory to path to import app modules
sys.path.append(str(Path(__file__).parent.parent))

from sqlalchemy import create_engine, text
from sqlalchemy.orm import Session
from app.core.config import settings

def run_migration():
    """Execute the migration"""
    # Create engine
    DATABASE_URL = f"postgresql://{settings.POSTGRES_USER}:{settings.POSTGRES_PASSWORD}@{settings.POSTGRES_SERVER}:{settings.POSTGRES_PORT}/{settings.POSTGRES_DB}"
    engine = create_engine(DATABASE_URL)
    
    print(f"Connecting to database: {settings.POSTGRES_DB}")
    print("Starting migration 002: Reverse User-Degree relationship...")
    
    try:
        with engine.begin() as connection:
            # Step 1: Remove FK constraint and column from users
            print("Step 1: Removing degree_id from users table...")
            connection.execute(text("""
                ALTER TABLE users DROP CONSTRAINT IF EXISTS users_degree_id_fkey;
            """))
            connection.execute(text("""
                DROP INDEX IF EXISTS ix_users_degree_id;
            """))
            connection.execute(text("""
                ALTER TABLE users DROP COLUMN IF EXISTS degree_id;
            """))
            print("  ✓ Removed degree_id column and constraints from users")
            
            # Step 2: Add jefe_carrera_user_id to degrees
            print("Step 2: Adding jefe_carrera_user_id to degrees table...")
            connection.execute(text("""
                ALTER TABLE degrees ADD COLUMN IF NOT EXISTS jefe_carrera_user_id INTEGER;
            """))
            print("  ✓ Added jefe_carrera_user_id column to degrees")
            
            # Step 3: Create UNIQUE constraint
            print("Step 3: Creating UNIQUE constraint...")
            connection.execute(text("""
                ALTER TABLE degrees 
                DROP CONSTRAINT IF EXISTS degrees_jefe_carrera_user_id_unique;
            """))
            connection.execute(text("""
                ALTER TABLE degrees 
                ADD CONSTRAINT degrees_jefe_carrera_user_id_unique 
                UNIQUE (jefe_carrera_user_id);
            """))
            print("  ✓ Created UNIQUE constraint on jefe_carrera_user_id")
            
            # Step 4: Create FK constraint
            print("Step 4: Creating foreign key constraint...")
            connection.execute(text("""
                ALTER TABLE degrees 
                DROP CONSTRAINT IF EXISTS degrees_jefe_carrera_user_id_fkey;
            """))
            connection.execute(text("""
                ALTER TABLE degrees 
                ADD CONSTRAINT degrees_jefe_carrera_user_id_fkey 
                FOREIGN KEY (jefe_carrera_user_id) 
                REFERENCES users(id) 
                ON DELETE SET NULL;
            """))
            print("  ✓ Created foreign key constraint")
            
            # Step 5: Create index
            print("Step 5: Creating index...")
            connection.execute(text("""
                CREATE INDEX IF NOT EXISTS ix_degrees_jefe_carrera_user_id 
                ON degrees(jefe_carrera_user_id);
            """))
            print("  ✓ Created index on jefe_carrera_user_id")
            
        print("\n✅ Migration 002 completed successfully!")
        print("\nNew schema:")
        print("  - users table: No longer has degree_id column")
        print("  - degrees table: Now has jefe_carrera_user_id column (UNIQUE)")
        print("  - Relationship: One JEFE_CARRERA user per degree (one-to-one)")
        
    except Exception as e:
        print(f"\n❌ Migration failed: {e}")
        raise

def rollback_migration():
    """Rollback the migration (restore original schema)"""
    DATABASE_URL = f"postgresql://{settings.POSTGRES_USER}:{settings.POSTGRES_PASSWORD}@{settings.POSTGRES_SERVER}:{settings.POSTGRES_PORT}/{settings.POSTGRES_DB}"
    engine = create_engine(DATABASE_URL)
    
    print(f"Connecting to database: {settings.POSTGRES_DB}")
    print("Rolling back migration 002...")
    
    try:
        with engine.begin() as connection:
            # Remove new column from degrees
            print("Step 1: Removing jefe_carrera_user_id from degrees...")
            connection.execute(text("""
                ALTER TABLE degrees DROP CONSTRAINT IF EXISTS degrees_jefe_carrera_user_id_fkey;
            """))
            connection.execute(text("""
                ALTER TABLE degrees DROP CONSTRAINT IF EXISTS degrees_jefe_carrera_user_id_unique;
            """))
            connection.execute(text("""
                DROP INDEX IF EXISTS ix_degrees_jefe_carrera_user_id;
            """))
            connection.execute(text("""
                ALTER TABLE degrees DROP COLUMN IF EXISTS jefe_carrera_user_id;
            """))
            print("  ✓ Removed jefe_carrera_user_id from degrees")
            
            # Restore degree_id to users
            print("Step 2: Restoring degree_id to users...")
            connection.execute(text("""
                ALTER TABLE users ADD COLUMN IF NOT EXISTS degree_id INTEGER;
            """))
            connection.execute(text("""
                ALTER TABLE users 
                ADD CONSTRAINT users_degree_id_fkey 
                FOREIGN KEY (degree_id) 
                REFERENCES degrees(id) 
                ON DELETE SET NULL;
            """))
            connection.execute(text("""
                CREATE INDEX IF NOT EXISTS ix_users_degree_id ON users(degree_id);
            """))
            print("  ✓ Restored degree_id to users")
            
        print("\n✅ Rollback completed successfully!")
        
    except Exception as e:
        print(f"\n❌ Rollback failed: {e}")
        raise

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Migration 002: Reverse User-Degree relationship")
    parser.add_argument("--rollback", action="store_true", help="Rollback the migration")
    
    args = parser.parse_args()
    
    if args.rollback:
        rollback_migration()
    else:
        run_migration()

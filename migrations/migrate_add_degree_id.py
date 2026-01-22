#!/usr/bin/env python3
"""
Script de migración: Agregar columna degree_id a la tabla users
Ejecutar: python migrations/migrate_add_degree_id.py
"""

import sys
import os

# Agregar el directorio raíz al path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy import text
from app.core.conexion import engine, SessionLocal


def migrate():
    """Ejecutar la migración"""
    print("Iniciando migración: Agregar columna degree_id a users...")
    
    with engine.connect() as connection:
        try:
            # Verificar si la columna ya existe
            result = connection.execute(text("""
                SELECT column_name 
                FROM information_schema.columns 
                WHERE table_name = 'users' AND column_name = 'degree_id'
            """))
            
            if result.fetchone():
                print("⚠️  La columna degree_id ya existe en la tabla users")
                return
            
            # Iniciar transacción
            print("1. Agregando columna degree_id...")
            connection.execute(text("""
                ALTER TABLE users 
                ADD COLUMN degree_id INTEGER
            """))
            
            print("2. Agregando foreign key constraint...")
            connection.execute(text("""
                ALTER TABLE users 
                ADD CONSTRAINT users_degree_id_fkey 
                FOREIGN KEY (degree_id) REFERENCES degrees(id)
            """))
            
            print("3. Creando índice...")
            connection.execute(text("""
                CREATE INDEX ix_users_degree_id ON users(degree_id)
            """))
            
            connection.commit()
            
            print("✅ Migración completada exitosamente")
            
            # Verificar
            result = connection.execute(text("""
                SELECT column_name, data_type, is_nullable 
                FROM information_schema.columns 
                WHERE table_name = 'users' AND column_name = 'degree_id'
            """))
            
            row = result.fetchone()
            if row:
                print(f"\n📊 Columna agregada:")
                print(f"   - Nombre: {row[0]}")
                print(f"   - Tipo: {row[1]}")
                print(f"   - Nullable: {row[2]}")
            
        except Exception as e:
            connection.rollback()
            print(f"❌ Error en la migración: {e}")
            raise


def rollback():
    """Revertir la migración"""
    print("Revirtiendo migración: Eliminando columna degree_id de users...")
    
    with engine.connect() as connection:
        try:
            print("1. Eliminando índice...")
            connection.execute(text("""
                DROP INDEX IF EXISTS ix_users_degree_id
            """))
            
            print("2. Eliminando foreign key constraint...")
            connection.execute(text("""
                ALTER TABLE users 
                DROP CONSTRAINT IF EXISTS users_degree_id_fkey
            """))
            
            print("3. Eliminando columna...")
            connection.execute(text("""
                ALTER TABLE users 
                DROP COLUMN IF EXISTS degree_id
            """))
            
            connection.commit()
            
            print("✅ Rollback completado exitosamente")
            
        except Exception as e:
            connection.rollback()
            print(f"❌ Error en rollback: {e}")
            raise


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "rollback":
        rollback()
    else:
        migrate()

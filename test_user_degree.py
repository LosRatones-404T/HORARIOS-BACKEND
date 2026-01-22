#!/usr/bin/env python3
"""
Script de ejemplo para probar la funcionalidad de usuarios y carreras.

Este script demuestra cómo:
1. Crear carreras
2. Crear un usuario JEFE_CARRERA con carrera asignada
3. Autenticar al usuario
4. Obtener información del usuario con su carrera
"""

import requests
import json
from typing import Optional

BASE_URL = "http://localhost:8000"

def print_response(title: str, response: requests.Response):
    """Imprime una respuesta formateada"""
    print(f"\n{'='*60}")
    print(f"{title}")
    print(f"{'='*60}")
    print(f"Status Code: {response.status_code}")
    try:
        print(f"Response: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
    except:
        print(f"Response: {response.text}")
    print(f"{'='*60}\n")


def create_admin_user():
    """Crear usuario admin si no existe"""
    print("\n🔧 Creando usuario ADMIN...")
    response = requests.post(
        f"{BASE_URL}/auth/register",
        json={
            "username": "admin",
            "email": "admin@unsis.edu.mx",
            "password": "admin123",
            "role": "ADMIN"
        }
    )
    if response.status_code == 201:
        print("✅ Usuario ADMIN creado exitosamente")
    elif response.status_code == 400 and "already registered" in response.text:
        print("ℹ️  Usuario ADMIN ya existe")
    else:
        print_response("❌ Error al crear ADMIN", response)
    return response


def login(username: str, password: str) -> Optional[str]:
    """Login y obtener token"""
    print(f"\n🔑 Autenticando usuario: {username}...")
    response = requests.post(
        f"{BASE_URL}/auth/login",
        data={
            "username": username,
            "password": password
        }
    )
    
    if response.status_code == 200:
        token = response.json()["access_token"]
        print(f"✅ Login exitoso. Token obtenido.")
        return token
    else:
        print_response("❌ Error en login", response)
        return None


def create_degree(token: str, name: str, jefe_carrera: str) -> Optional[dict]:
    """Crear una nueva carrera"""
    print(f"\n📚 Creando carrera: {name}...")
    response = requests.post(
        f"{BASE_URL}/degrees/",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "name": name,
            "jefe_carrera": jefe_carrera,
            "is_active": True
        }
    )
    
    if response.status_code == 201:
        degree = response.json()
        print(f"✅ Carrera creada: {degree['name']} (ID: {degree['id']})")
        return degree
    else:
        print_response("❌ Error al crear carrera", response)
        return None


def create_jefe_carrera(token: str, username: str, email: str, password: str, degree_id: int) -> Optional[dict]:
    """Crear un usuario JEFE_CARRERA con carrera asignada"""
    print(f"\n👤 Creando jefe de carrera: {username}...")
    response = requests.post(
        f"{BASE_URL}/auth/register",
        json={
            "username": username,
            "email": email,
            "password": password,
            "role": "JEFE_CARRERA",
            "degree_id": degree_id
        }
    )
    
    if response.status_code == 201:
        user = response.json()
        print(f"✅ Jefe de carrera creado: {user['username']}")
        return user
    else:
        print_response("❌ Error al crear jefe de carrera", response)
        return None


def get_current_user(token: str) -> Optional[dict]:
    """Obtener información del usuario actual"""
    print(f"\n👤 Obteniendo información del usuario actual...")
    response = requests.get(
        f"{BASE_URL}/auth/me",
        headers={"Authorization": f"Bearer {token}"}
    )
    
    if response.status_code == 200:
        user = response.json()
        print(f"✅ Usuario obtenido: {user['username']}")
        return user
    else:
        print_response("❌ Error al obtener usuario", response)
        return None


def main():
    print("\n" + "🚀 " * 20)
    print("Demostración: Usuarios y Carreras")
    print("🚀 " * 20)
    
    # Paso 1: Crear usuario admin
    create_admin_user()
    
    # Paso 2: Login como admin
    admin_token = login("admin", "admin123")
    if not admin_token:
        print("\n❌ No se pudo autenticar como admin. Verifica que el servidor esté corriendo.")
        return
    
    # Paso 3: Crear carreras
    degree1 = create_degree(
        admin_token,
        "Ingeniería en Sistemas Computacionales",
        "Dr. Juan Pérez González"
    )
    
    degree2 = create_degree(
        admin_token,
        "Ingeniería Industrial",
        "Mtro. Carlos López Martínez"
    )
    
    if not degree1:
        print("\n⚠️  No se pudo crear la carrera. Puede que ya exista.")
        print("Continuando con el ejemplo usando ID de carrera 1...")
        degree_id = 1
    else:
        degree_id = degree1["id"]
    
    # Paso 4: Crear jefe de carrera
    jefe = create_jefe_carrera(
        admin_token,
        "jefe_sistemas",
        "jefe.sistemas@unsis.edu.mx",
        "password123",
        degree_id
    )
    
    if jefe:
        print(f"\n📋 Información del jefe de carrera creado:")
        print(f"   - Username: {jefe['username']}")
        print(f"   - Email: {jefe['email']}")
        print(f"   - Role: {jefe['role']}")
        print(f"   - Carrera ID: {jefe.get('degree_id')}")
        if jefe.get('degree'):
            print(f"   - Carrera: {jefe['degree']['name']}")
    
    # Paso 5: Login como jefe de carrera
    jefe_token = login("jefe_sistemas", "password123")
    if not jefe_token:
        print("\n⚠️  No se pudo autenticar como jefe de carrera.")
        return
    
    # Paso 6: Obtener información del jefe de carrera
    user_info = get_current_user(jefe_token)
    
    if user_info:
        print("\n" + "📊 " * 20)
        print("INFORMACIÓN COMPLETA DEL JEFE DE CARRERA")
        print("📊 " * 20)
        print(f"\n{json.dumps(user_info, indent=2, ensure_ascii=False)}")
        
        if user_info.get('degree'):
            print("\n✅ ÉXITO: El jefe de carrera tiene acceso a la información de su carrera:")
            print(f"   🎓 Carrera: {user_info['degree']['name']}")
            print(f"   👨‍🏫 Jefe actual: {user_info['degree']['jefe_carrera']}")
            print(f"   ✓ Activa: {user_info['degree']['is_active']}")
        else:
            print("\n⚠️  El usuario no tiene carrera asignada")
    
    print("\n" + "✅ " * 20)
    print("Demostración completada exitosamente")
    print("✅ " * 20)
    print("\n📖 Próximos pasos:")
    print("   1. Usa el token del jefe de carrera para filtrar datos por carrera")
    print("   2. Implementa dashboards específicos por carrera")
    print("   3. Consulta la documentación en docs/USER_DEGREE_INTEGRATION.md")
    print()


if __name__ == "__main__":
    try:
        main()
    except requests.exceptions.ConnectionError:
        print("\n❌ Error: No se pudo conectar al servidor.")
        print("   Asegúrate de que el servidor esté corriendo en http://localhost:8000")
    except Exception as e:
        print(f"\n❌ Error inesperado: {e}")
        import traceback
        traceback.print_exc()

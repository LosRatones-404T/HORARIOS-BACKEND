# Gestión de Carreras y Jefes de Carrera

## Descripción General

Este módulo permite gestionar las carreras académicas y mantener actualizada la información sobre qué profesor está actualmente ejerciendo como jefe de carrera.

## Concepto Clave

El sistema distingue entre:

1. **Usuarios con rol `JEFE_CARRERA`**: Son usuarios permanentes del sistema que tienen permisos para realizar ciertas operaciones. Estos usuarios NO cambian con el tiempo.

2. **Campo `jefe_carrera` en la tabla `Degree`**: Es un campo de texto que indica el nombre del profesor que actualmente está en turno como jefe de carrera de esa carrera específica. Este valor SÍ cambia cuando hay relevo en el cargo.

## Ejemplo de Uso

### Escenario:
- Juan Pérez es un usuario del sistema con rol `JEFE_CARRERA`
- María González también es un usuario con rol `JEFE_CARRERA`
- Ambos tienen acceso a las funciones del sistema

Cuando Juan Pérez termina su periodo como jefe de la carrera de "Ingeniería en Sistemas" y María González toma el cargo:

- Los usuarios del sistema NO cambian (ambos siguen teniendo rol `JEFE_CARRERA`)
- Solo se actualiza el campo `jefe_carrera` de la carrera de "Ingeniería en Sistemas" de "Juan Pérez" a "María González"

## Endpoints Principales

### Actualizar Jefe de Carrera en Turno

```bash
PATCH /degrees/{degree_id}/jefe-carrera
```

Este es el endpoint más importante para tu caso de uso. Permite actualizar únicamente el nombre del profesor que está en turno como jefe de carrera.

**Ejemplo:**
```bash
curl -X PATCH http://localhost:8000/degrees/1/jefe-carrera \
  -H "Authorization: Bearer <jwt>" \
  -H "Content-Type: application/json" \
  -d '{"jefe_carrera":"Dra. María González Rodríguez"}'
```

**Permisos requeridos:** `ADMIN` o `JEFE_CARRERA`

### Consultar Carreras

```bash
GET /degrees/
GET /degrees/active
GET /degrees/{degree_id}
```

Estos endpoints permiten consultar la información de las carreras, incluyendo quién es el jefe de carrera actual.

**Permisos requeridos:** Cualquier usuario autenticado

### Gestión Completa de Carreras

Para administradores, existen endpoints adicionales para:
- Crear nuevas carreras (`POST /degrees/`)
- Actualizar información completa (`PUT /degrees/{degree_id}`)
- Cambiar estado activo/inactivo (`PATCH /degrees/{degree_id}/toggle-status`)
- Eliminar carreras (`DELETE /degrees/{degree_id}`)

**Permisos requeridos:** `ADMIN`

## Estructura de Datos

### Modelo Degree
```python
class Degree(Base):
    __tablename__ = "degrees"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True, nullable=False)
    jefe_carrera = Column(String, nullable=True)  # Profesor en turno
    is_active = Column(Boolean, default=True)
```

## Flujo de Trabajo Recomendado

1. **Al inicio del semestre/periodo:**
   - Verificar las carreras activas: `GET /degrees/active`
   - Para cada carrera que tenga un nuevo jefe, actualizar: `PATCH /degrees/{id}/jefe-carrera`

2. **Durante el periodo:**
   - Los usuarios con rol `JEFE_CARRERA` mantienen sus permisos
   - El campo `jefe_carrera` en cada carrera refleja quién está a cargo

3. **Reportes y documentos:**
   - Al generar documentos oficiales, consultar `GET /degrees/{id}` para obtener el nombre correcto del jefe de carrera actual

## Ventajas de este Diseño

✅ **Separación de conceptos**: Los permisos del sistema (usuarios) están separados de los datos académicos (quién está en el cargo)

✅ **Flexibilidad**: Un mismo usuario puede ser jefe de múltiples carreras si es necesario

✅ **Historial**: Si se implementa auditoría, se puede rastrear cuándo cambió cada jefe de carrera

✅ **Simplicidad**: Los cambios de turno son operaciones simples que no afectan la autenticación ni permisos

## Documentación Adicional

Para más detalles sobre los endpoints, consulta [docs/API.md](../docs/API.md#carreras-degrees)

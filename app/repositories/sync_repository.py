# repositories/sync_repository.py
from sqlalchemy.orm import Session
from app.models.unsis import Carrera, Grupo, Periodo, Aula, Profesor, Materia, Horario

class SyncRepository:
    def __init__(self, db: Session):
        self.db = db

    def upsert_carrera(self, data: dict):
        # Buscamos si existe por clave
        obj = self.db.query(Carrera).filter(Carrera.clave == data["clave"]).first()
        if obj:
            # Actualizamos campos
            for key, value in data.items():
                setattr(obj, key, value)
        else:
            # Creamos nuevo
            obj = Carrera(**data)
            self.db.add(obj)
        # No hacemos commit aquí para poder hacer rollback si algo falla en lote
        return obj

    def upsert_periodo(self, data: dict):
        obj = self.db.query(Periodo).filter(Periodo.clave == data["clave"]).first()
        if obj:
            for k, v in data.items():
                setattr(obj, k, v)
        else:
            self.db.add(Periodo(**data))

    def upsert_grupo(self, data: dict):
        # OJO: En tu modelo la columna se llama 'carrera_id', en el JSON 'carrera'
        # Hacemos el mapeo manual
        grupo_data = data.copy()
        grupo_data['carrera_id'] = grupo_data.pop('carrera') # Cambia llave 'carrera' a 'carrera_id'
        grupo_data['periodo_id'] = grupo_data.pop('periodo')
        
        obj = self.db.query(Grupo).filter(Grupo.clave == grupo_data["clave"]).first()
        if obj:
            for k, v in grupo_data.items():
                setattr(obj, k, v)
        else:
            self.db.add(Grupo(**grupo_data))

    def upsert_aula(self, data:dict):

        obj = self.db.query(Aula).filter(Aula.clave == data["clave"]).first()
        if obj:
            for k, v in data.items():
                setattr(obj, k, v)
        else:
            self.db.add(Aula(**data))

    def upsert_profesor(self, id_prof, nombre):
        if not id_prof: return None
        obj = self.db.query(Profesor).filter(Profesor.id == id_prof).first()
        if not obj:
            obj = Profesor(id=id_prof, nombre=nombre)
            self.db.add(obj)
            self.db.flush() # Para que esté disponible inmediatamente en la sesión
        return obj

    def upsert_materia(self, id_mat, nombre):
        if not id_mat: return None
        obj = self.db.query(Materia).filter(Materia.id == id_mat).first()
        if not obj:
            obj = Materia(id=id_mat, nombre=nombre)
            self.db.add(obj)
            self.db.flush()
        return obj

    def upsert_horario(self, item: dict):
        # 1. Asegurar dependencias
        self.upsert_profesor(item.get('idprofesor'), item.get('nombreCompleto'))
        self.upsert_materia(item.get('asignatura'), item.get('materia'))
        
        # 2. Guardar Horario
        horario_id = item['rowId']
        obj = self.db.query(Horario).filter(Horario.id == horario_id).first()
        
        # Datos limpios para el modelo
        datos_horario = {
            "id": horario_id,
            "dia": item['dia'],
            "hora": item['hora'],
            "grupo_id": item['idGrupo'],
            "aula_id": item['idAula'] if item['idAula'] else None, # Manejar vacíos
            "profesor_id": item['idprofesor'],
            "materia_id": item['asignatura']
        }

        if obj:
            for k, v in datos_horario.items():
                setattr(obj, k, v)
        else:
            self.db.add(Horario(**datos_horario))
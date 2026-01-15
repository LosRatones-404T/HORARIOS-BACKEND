# repositories/sync_repository.py
from sqlalchemy.orm import Session
from app.models.unsis import Carrera, Grupo, Periodo, Aula

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
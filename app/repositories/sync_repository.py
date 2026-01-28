# repositories/sync_repository.py
from sqlalchemy.orm import Session
from app.models.unsis import Carrera, Grupo, Periodo, Aula, Profesor, Materia, Horario

class SyncRepository:
    def __init__(self, db: Session):
        self.db = db

    def upsert_carrera(self, data: dict):
        obj = self.db.query(Carrera).filter(Carrera.clave == data["clave"]).first()
        
        # Campos principales del modelo
        main_fields = {'clave', 'nombre', 'vigente'}
        main_data = {k: v for k, v in data.items() if k in main_fields}
        
        if obj:
            for key, value in main_data.items():
                setattr(obj, key, value)
        else:
            obj = Carrera(**main_data)
            self.db.add(obj)
        return obj

    def upsert_periodo(self, data: dict):
        obj = self.db.query(Periodo).filter(Periodo.clave == data["clave"]).first()
        if obj:
            for k, v in data.items():
                if hasattr(Periodo, k):
                    setattr(obj, k, v)
        else:
            valid_fields = {c.name for c in Periodo.__table__.columns}
            filtered_data = {k: v for k, v in data.items() if k in valid_fields}
            self.db.add(Periodo(**filtered_data))

    def upsert_grupo(self, data: dict):
        grupo_data = data.copy()
        grupo_data['carrera_id'] = grupo_data.pop('carrera')
        grupo_data['periodo_id'] = grupo_data.pop('periodo')
        
        # Campos principales
        main_fields = {'clave', 'nombre', 'semestre', 'cupo', 'carrera_id', 'periodo_id'}
        main_data = {k: v for k, v in grupo_data.items() if k in main_fields}
        
        # Campos adicionales (todo lo demás)
        extra_data = {k: v for k, v in grupo_data.items() if k not in main_fields}
        
        obj = self.db.query(Grupo).filter(Grupo.clave == main_data["clave"]).first()
        if obj:
            for k, v in main_data.items():
                setattr(obj, k, v)
            # Guardar campos adicionales como JSON
            if extra_data:
                obj.datos_adicionales = extra_data
        else:
            new_grupo = Grupo(**main_data)
            if extra_data:
                new_grupo.datos_adicionales = extra_data
            self.db.add(new_grupo)

    def upsert_aula(self, data: dict):
        obj = self.db.query(Aula).filter(Aula.clave == data["clave"]).first()
        
        valid_fields = {'clave', 'nombre', 'capacidad', 'tipo', 'statusProyector'}
        filtered_data = {k: v for k, v in data.items() if k in valid_fields}
        
        if obj:
            for k, v in filtered_data.items():
                setattr(obj, k, v)
        else:
            self.db.add(Aula(**filtered_data))

    def upsert_profesor(self, id_prof, nombre):
        if not id_prof:
            return None
        obj = self.db.query(Profesor).filter(Profesor.id == id_prof).first()
        if not obj:
            obj = Profesor(id=id_prof, nombre=nombre)
            self.db.add(obj)
            self.db.flush()
        return obj

    def upsert_materia(self, id_mat, nombre):
        if not id_mat:
            return None
        obj = self.db.query(Materia).filter(Materia.id == id_mat).first()
        if not obj:
            obj = Materia(id=id_mat, nombre=nombre)
            self.db.add(obj)
            self.db.flush()
        return obj

    def upsert_horario(self, item: dict):
        self.upsert_profesor(item.get('idprofesor'), item.get('nombreCompleto'))
        self.upsert_materia(item.get('asignatura'), item.get('materia'))
        
        horario_id = item['rowId']
        obj = self.db.query(Horario).filter(Horario.id == horario_id).first()
        
        datos_horario = {
            "id": horario_id,
            "dia": item['dia'],
            "hora": item['hora'],
            "grupo_id": item['idGrupo'],
            "aula_id": item.get('idAula') if item.get('idAula') else None,
            "profesor_id": item.get('idprofesor'),
            "materia_id": item['asignatura']
        }

        if obj:
            for k, v in datos_horario.items():
                setattr(obj, k, v)
        else:
            self.db.add(Horario(**datos_horario))
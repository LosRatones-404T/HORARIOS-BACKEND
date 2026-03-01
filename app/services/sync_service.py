# services/sync_service.py
import requests
import os
from sqlalchemy.orm import Session
from app.repositories.sync_repository import SyncRepository
from app.schemas.sync_schemas import AulaSchema, CarreraSchema, GrupoSchema, PeriodoSchema

class SyncService:
    def __init__(self, db: Session):
        self.repo = SyncRepository(db)
        # Usar variable de entorno, con fallback a host.docker.internal para Docker
        # self.base_url = os.getenv("EXTERNAL_API_URL", "http://host.docker.internal:3000/api")
        self.base_url = os.getenv("EXTERNAL_API_URL", "http://10.42.0.152:3000/api")

    def sync_all(self):
        try:
            # 1. Traer y Guardar Periodo (Indispensable para Grupos)
            print("Sincronizando Periodos...")
            p_data = self._fetch_data("/periodo/actual") # Supongamos que devuelve un dict directo
            # Validar con Pydantic
            periodo_valido = PeriodoSchema(**p_data)
            self.repo.upsert_periodo(periodo_valido.model_dump())

            # Traer y Guardar Aulas
            print("Sincronizando Aulas...")
            a_data_list = self._fetch_data("/aulas")
            for a in a_data_list:
                aula_valida = AulaSchema(**a)
                self.repo.upsert_aula(aula_valida.model_dump())

            # 2. Traer y Guardar Carreras (Indispensable para Grupos)
            print("Sincronizando Carreras...")
            c_data_list = self._fetch_data("/carreras/vigentes")
            for c in c_data_list:
                c_valido = CarreraSchema(**c)
                self.repo.upsert_carrera(c_valido.model_dump())
            
            # 3. Traer y Guardar Grupos (Ya existen sus papás)
            print("Sincronizando Grupos...")

            g_data_list = self._fetch_data("/grupos/periodo='clave'")
            for g in g_data_list:
                g_valido = GrupoSchema(**g)
                self.repo.upsert_grupo(g_valido.model_dump())

            print("Sincronizando Horarios Completos...")
            
            # endpoint ej: /horarios_completos
            data_dict = self._fetch_data("/horarios/todos") 
            
            # El JSON es un Dict: {"104-A": [obj, obj], "106-A": [...]}
            # Iteramos sobre las llaves (Grupos)
            for grupo_key, lista_horarios in data_dict.items():
                
                for item in lista_horarios:
                    # Validar datos básicos (opcional usar Schema aquí)
                    # upsert
                    self.repo.upsert_horario(item)

            # Confirmar cambios en BD
            self.repo.db.commit()
            return {"status": "Sincronización exitosa"}

        except Exception as e:
            self.repo.db.rollback() # Deshacer cambios si algo falló
            print(f"Error crítico: {e}")
            raise e

    def _fetch_data(self, endpoint):
        # Aquí manejas los headers, tokens, y la conexión
        # Como vimos antes, verifica si necesitas verify=False por ser .lan
        response = requests.get(f"{self.base_url}{endpoint}", verify=False)
        response.raise_for_status()
        return response.json()
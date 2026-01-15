from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.conexion import get_db
from app.services.sync_service import SyncService

router = APIRouter(prefix="/sync", tags=["sync"])

@router.post("/sincronizar-todo", status_code=201)
def trigger_sync(db: Session = Depends(get_db)):
    sync_service = SyncService(db)
    result = sync_service.sync_all()
    return result
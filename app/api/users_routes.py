from datetime import timedelta
from re import U
from urllib import response
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.schemas.user_schemas import UserCreate, UserRead, Token
from app.services.user_service import change_user_email, update_user_password, toggle_user_active_status, get_all_users, change_user_role
from app.dependencies import get_db
from app.core.security import get_current_user

router = APIRouter(prefix="/users", tags=["users"])



@router.post("/update-password", response_model=UserRead)
# actualizar contraseña de usuario especificado
def password_update(username: str, new_password: str, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    """
    Actualiza la contraseña del usuario especificado.
    """
    user = update_user_password(db, username, new_password)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

# obtener todos los usuarios
@router.get("/", response_model=list[UserRead])
def read_users(db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    """
    Obtiene todos los usuarios.
    """
    users = get_all_users(db)
    return users

# cambiar rol de usuario especificado
@router.put("/change-role", response_model=UserRead)
def change_role(username: str, new_role: str, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    """
    Cambia el rol del usuario especificado.
    """

    user = change_user_role(db, username, new_role)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

# cambiar estado activo de usuario especificado
@router.put("/toggle-active", response_model=UserRead)
def toggle_active(username: str, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    """
    Cambia el estado activo del usuario especificado.
    """
    user = toggle_user_active_status(db, username)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

# cambiar email de usuario especificado
@router.put("/change-email", response_model=UserRead)
def change_email(username: str, new_email: str, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    """
    Cambia el email del usuario especificado.
    """
    user = change_user_email(db, username, new_email)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user
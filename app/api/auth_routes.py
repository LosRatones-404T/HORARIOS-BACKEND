from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.schemas.user_schemas import UserCreate, UserRead, Token, UserCreateJefe
from app.services.user_service import register_user, authenticate_user, create_token_for_user, register_user_jefe
from app.dependencies import get_db
from app.core.security import get_current_user

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register", response_model=UserRead, status_code=status.HTTP_201_CREATED)
def register(user_in: UserCreate, db: Session = Depends(get_db)):
    print("Registering user:", user_in.username)
    existing = authenticate_user(db, user_in.username, user_in.password)
    # simple check: username must be unique
    from app.repositories.user_repository import get_user_by_username

    if get_user_by_username(db, user_in.username):
        raise HTTPException(status_code=400, detail="Username already registered")
    user = register_user(db, user_in)
    return user

@router.post("/register-jefe_carrera", response_model=UserRead, status_code=status.HTTP_201_CREATED)
def register_jefe(user_in: UserCreateJefe, db: Session = Depends(get_db)):
    print("Registering user:", user_in.username)
    existing = authenticate_user(db, user_in.username, user_in.password)
    # simple check: username must be unique
    from app.repositories.user_repository import get_user_by_username

    if get_user_by_username(db, user_in.username):
        raise HTTPException(status_code=400, detail="Username already registered")
    user = register_user_jefe(db, user_in)
    return user


@router.post("/login", response_model=Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    access_token_expires = timedelta(minutes=60)
    access_token = create_token_for_user(user, expires_delta=access_token_expires)
    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/me", response_model=UserRead)
def read_users_me(current_user=Depends(get_current_user)):
    return current_user

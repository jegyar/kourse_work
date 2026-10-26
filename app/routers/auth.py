from fastapi import APIRouter, Depends, HTTPException, status
import psycopg2.extensions
from fastapi.security import OAuth2PasswordRequestForm
from datetime import timedelta

from app.database import get_db_dependency
from app.models.user import UserCreate, UserResponse, Token
from app.services.auth_service import AuthService
from app.utils.security import create_access_token
from app.config import settings

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)


@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def register(user_data: UserCreate, conn: psycopg2.extensions.connection = Depends(get_db_dependency)):
    """Регистрация нового пользователя."""
    auth_service = AuthService(conn)
    return auth_service.register_user(user_data)


@router.post("/login", response_model=Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), conn: psycopg2.extensions.connection = Depends(get_db_dependency)):
    """Вход пользователя и получение JWT токена."""
    # Переиспользуем модель UserLogin, маппя данные из формы OAuth2
    from app.models.user import UserLogin
    login_data = UserLogin(email=form_data.username, password=form_data.password)
    
    auth_service = AuthService(conn)
    user = auth_service.authenticate_user(login_data)
    
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user["email"], "role_id": user["role_id"]},
        expires_delta=access_token_expires
    )
    
    return {"access_token": access_token, "token_type": "bearer"}

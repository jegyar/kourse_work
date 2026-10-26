from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
import bcrypt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
import psycopg2.extensions

from app.config import settings
from app.database import get_db_dependency
from app.models.user import TokenData, UserResponse

# Зависимость для извлечения токена из заголовка Authorization
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Проверка соответствия пароля хешу."""
    return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))


def get_password_hash(password: str) -> str:
    """Генерация хеша из пароля."""
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """Генерация JWT токена."""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)

    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt


async def get_current_user(
    token: str = Depends(oauth2_scheme),
    conn: psycopg2.extensions.connection = Depends(get_db_dependency)
) -> UserResponse:
    """Извлечение и валидация текущего пользователя из токена."""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Не удалось проверить учетные данные",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
        token_data = TokenData(email=email, role_id=payload.get("role_id"))
    except JWTError:
        raise credentials_exception

    cursor = conn.cursor()
    cursor.execute(
        """
        SELECT user_id, email, first_name, last_name, role_id, created_at 
        FROM "User" WHERE email = %s
        """,
        (token_data.email,)
    )
    row = cursor.fetchone()

    if row is None:
        raise credentials_exception

    return UserResponse(
        user_id=row[0],
        email=row[1],
        first_name=row[2],
        last_name=row[3],
        role_id=row[4],
        created_at=row[5]
    )


async def get_current_admin_user(current_user: UserResponse = Depends(get_current_user)) -> UserResponse:
    """Проверка, является ли текущий пользователь администратором."""
    if current_user.role_id != 1:  # 1 = admin, 2 = client (согласно seed.sql)
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Недостаточно прав. Требуется роль администратора."
        )
    return current_user


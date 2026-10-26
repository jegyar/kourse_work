import psycopg2.extensions
from fastapi import HTTPException, status
from app.models.user import UserCreate, UserLogin, UserResponse
from app.utils.security import get_password_hash, verify_password


class AuthService:
    def __init__(self, conn: psycopg2.extensions.connection):
        self.conn = conn
        self.cursor = self.conn.cursor()

    def register_user(self, user_data: UserCreate) -> UserResponse:
        """Регистрация нового пользователя."""
        # Проверка, существует ли уже пользователь с таким email
        self.cursor.execute('SELECT user_id FROM "User" WHERE email = %s', (user_data.email,))
        if self.cursor.fetchone():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Пользователь с таким email уже существует"
            )

        hashed_password = get_password_hash(user_data.password)

        # Вставка нового пользователя. role_id по умолчанию 2 (client) согласно схеме.
        self.cursor.execute(
            """
            INSERT INTO "User" (email, password_hash, first_name, last_name)
            VALUES (%s, %s, %s, %s)
            RETURNING user_id, email, first_name, last_name, role_id, created_at
            """,
            (user_data.email, hashed_password, user_data.first_name, user_data.last_name)
        )
        row = self.cursor.fetchone()
        self.conn.commit()

        return UserResponse(
            user_id=row[0],
            email=row[1],
            first_name=row[2],
            last_name=row[3],
            role_id=row[4],
            created_at=row[5]
        )

    def authenticate_user(self, login_data: UserLogin) -> dict:
        """Аутентификация пользователя и возврат данных для токена."""
        self.cursor.execute(
            """
            SELECT user_id, email, password_hash, role_id 
            FROM "User" WHERE email = %s
            """,
            (login_data.email,)
        )
        row = self.cursor.fetchone()

        if not row or not verify_password(login_data.password, row[2]):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Неверный email или пароль",
                headers={"WWW-Authenticate": "Bearer"},
            )

        return {
            "user_id": row[0],
            "email": row[1],
            "role_id": row[3]
        }

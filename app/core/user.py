import logging
from typing import Optional, Union

from fastapi import Depends, HTTPException, Request, status
from fastapi_users import (
    BaseUserManager,
    FastAPIUsers,
    InvalidPasswordException,
)
from fastapi_users.authentication import (
    AuthenticationBackend,
    BearerTransport,
    JWTStrategy,
)
from fastapi_users_db_sqlalchemy import SQLAlchemyUserDatabase

from app.models.user import User
from app.schemas.user import UserCreate
from app.core.db import AsyncSession, get_async_session


SECRET = "SECRET"

bearer_transport = BearerTransport(tokenUrl="auth/jwt/login")


def get_jwt_strategy() -> JWTStrategy:
    """Возвращает стратегию JWT с секретом и сроком жизни токена."""
    return JWTStrategy(secret=SECRET, lifetime_seconds=3600)


auth_backend = AuthenticationBackend(
    name="jwt",
    transport=bearer_transport,
    get_strategy=get_jwt_strategy,
)


async def get_user_db(session: AsyncSession = Depends(get_async_session)):
    """Асинхронно возвращает пользовательскую базу данных."""
    yield SQLAlchemyUserDatabase(session, User)


class UserManager(BaseUserManager[User, int]):
    """_summary_

    Аргументы:
        BaseUserManager (_type_): _description_

    Вызывает:
        InvalidPasswordException: _description_
        InvalidPasswordException: _description_
        InvalidPasswordException: _description_
        HTTPException: _description_

    Возвращает:
        _type_: _description_
    """
    user_db_model = User

    async def validate_password(
        self,
        password: str,
        user: Union[UserCreate, User],
    ) -> None:
        if len(password) < 3:
            raise InvalidPasswordException(
                reason="Пароль должен быть не менее 3 символов"
            )
        if user.email in password:
            raise InvalidPasswordException(
                reason="Пароль не должен содержать email"
            )
        if password.isdigit():
            raise InvalidPasswordException(
                reason="Пароль не должен состоять только из цифр"
            )

    async def on_after_register(
        self, user: User,
        request: Optional[Request] = None
    ) -> None:
        """Логирует регистрацию пользователя."""
        logging.info(f"Пользователь {user.email} зарегистрирован.")

    def parse_id(self, user_id: str) -> int:
        """Парсит id пользователя в int или бросает 404."""
        try:
            return int(user_id)
        except ValueError:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Invalid user id: {user_id}"
            )


async def get_user_manager(user_db=Depends(get_user_db)):
    """Возвращает менеджер пользователя."""
    yield UserManager(user_db)


fastapi_users = FastAPIUsers[User, int](
    get_user_manager,
    [auth_backend],
)

current_user = fastapi_users.current_user()
current_superuser = fastapi_users.current_user(superuser=True)

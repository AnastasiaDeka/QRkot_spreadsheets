from fastapi import Depends
from fastapi.exceptions import HTTPException
from starlette import status

from app.models import User
from app.core.user import current_superuser

SUPERUSER_ERROR = HTTPException(
    status_code=status.HTTP_403_FORBIDDEN,
    detail="Недостаточно прав"
)


async def current_superuser(
    current_user: User = Depends(current_superuser)
) -> User:
    """Проверяет, что пользователь — суперпользователь."""
    if not current_user.is_superuser:
        raise SUPERUSER_ERROR
    return current_user

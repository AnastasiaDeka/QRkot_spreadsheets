from datetime import datetime
from typing import Optional

from pydantic import BaseModel, PositiveInt


class DonationBase(BaseModel):
    """Базовая схема пожертвования."""
    full_amount: PositiveInt
    comment: Optional[str] = None


class DonationCreate(DonationBase):
    """Схема создания пожертвования."""
    pass


class DonationUpdate(BaseModel):
    """Схема обновления пожертвования."""
    full_amount: Optional[PositiveInt] = None
    comment: Optional[str] = None


class DonationDB(DonationBase):
    """Схема пожертвования из базы с доп. полями."""
    id: int
    user_id: int
    invested_amount: int
    fully_invested: bool
    create_date: datetime
    close_date: Optional[datetime]

    class Config:
        orm_mode = True


class DonationUserView(BaseModel):
    """Отображение пожертвования для пользователя."""
    id: int
    full_amount: int
    comment: Optional[str]
    create_date: datetime

    class Config:
        orm_mode = True

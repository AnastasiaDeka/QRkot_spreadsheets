from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field, PositiveInt, validator, Extra


NAME_MIN_LENGTH = 1
NAME_MAX_LENGTH = 100


class CharityProjectBase(BaseModel):
    """Базовая схема проекта с обязательными полями."""
    name: str = Field(
        ...,
        min_length=NAME_MIN_LENGTH,
        max_length=NAME_MAX_LENGTH
    )
    description: str
    full_amount: PositiveInt


class CharityProjectCreate(CharityProjectBase):
    """Схема создания проекта с валидацией описания."""
    @validator('description')
    def description_not_empty(cls, value):
        if not value.strip():
            raise ValueError('Описание не может быть пустым')
        return value


class CharityProjectUpdate(BaseModel):
    """Схема обновления проекта с опциональными полями и запретом лишних."""
    name: Optional[str] = Field(
        None,
        min_length=NAME_MIN_LENGTH,
        max_length=NAME_MAX_LENGTH
    )
    description: Optional[str] = None
    full_amount: Optional[PositiveInt] = None

    class Config:
        extra = Extra.forbid

    @validator('name')
    def name_not_empty(cls, value):
        if value is not None and not value.strip():
            raise ValueError('Имя не может быть пустым')
        return value

    @validator('description')
    def description_not_empty(cls, value):
        if value is not None and not value.strip():
            raise ValueError('Описание не может быть пустым')
        return value


class CharityProjectDB(CharityProjectBase):
    """Схема проекта для чтения из базы с дополнительными полями."""
    id: int
    invested_amount: int
    fully_invested: bool
    create_date: Optional[datetime]
    close_date: Optional[datetime]

    class Config:
        orm_mode = True

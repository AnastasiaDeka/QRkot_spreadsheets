from typing import Generic, TypeVar, Type, List, Optional, Union

from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select


ModelType = TypeVar("ModelType")
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


class CRUDBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    def __init__(self, model: Type[ModelType]):
        """
        Инициализация CRUD с SQLAlchemy моделью.
        :param model: SQLAlchemy модель
        """
        self.model = model

    async def get(self, db: AsyncSession, id: int) -> Optional[ModelType]:
        """
        Получить объект по ID.
        :param db: сессия базы данных
        :param id: ID объекта
        :return: объект модели или None
        """
        result = await db.execute(
            select(self.model).filter(self.model.id == id)
        )
        return result.scalars().first()

    async def get_multi(self, db: AsyncSession) -> List[ModelType]:
        """
        Получить все объекты модели.
        :param db: сессия базы данных
        :return: список объектов модели
        """
        result = await db.execute(select(self.model))
        return result.scalars().all()

    async def create(
        self,
        db: AsyncSession,
        obj_in: CreateSchemaType,
        commit: bool = True
    ) -> ModelType:
        """
        Создать новый объект из схемы Pydantic.
        :param db: сессия базы данных
        :param obj_in: данные для создания
        :param commit: коммитить изменения сразу или нет
        :return: созданный объект модели
        """
        obj_in_data = obj_in.dict()
        db_obj = self.model(**obj_in_data)
        db.add(db_obj)
        if commit:
            await db.commit()
            await db.refresh(db_obj)
        return db_obj

    async def update(
        self,
        db: AsyncSession,
        db_obj: ModelType,
        obj_in: Union[UpdateSchemaType, dict]
    ) -> ModelType:
        """
        Обновить объект модели.
        :param db: сессия базы данных
        :param db_obj: существующий объект
        :param obj_in: данные для обновления (схема или dict)
        :return: обновленный объект модели
        """
        obj_data = db_obj.__dict__
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)
        for field in update_data:
            if field in obj_data:
                setattr(db_obj, field, update_data[field])
        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj

    async def remove(self, db: AsyncSession, id: int) -> Optional[ModelType]:
        """
        Удалить объект по ID.
        :param db: сессия базы данных
        :param id: ID объекта
        :return: удалённый объект или None
        """
        obj = await self.get(db, id)
        if obj:
            await db.delete(obj)
            await db.commit()
        return obj

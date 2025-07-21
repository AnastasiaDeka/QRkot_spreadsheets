from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.models.charity_project import CharityProject
from app.schemas.charity_project import (
    CharityProjectCreate,
    CharityProjectUpdate,
)


class CRUDCharityProject(
    CRUDBase[CharityProject, CharityProjectCreate, CharityProjectUpdate]
):
    """
    CRUD для CharityProject с проверкой уникальности имени.
    """

    async def create(
        self,
        db: AsyncSession,
        obj_in: CharityProjectCreate,
    ) -> CharityProject:
        """
        Создает проект, проверяя уникальность имени.
        """
        existing_project = await db.execute(
            select(CharityProject).where(
                CharityProject.name == obj_in.name
            )
        )
        if existing_project.scalar_one_or_none():
            raise HTTPException(
                status_code=400,
                detail="Проект с таким именем уже существует."
            )
        return await super().create(db, obj_in)

    async def update(
        self,
        db: AsyncSession,
        db_obj: CharityProject,
        obj_in: CharityProjectUpdate
    ) -> CharityProject:
        """
        Обновляет проект, проверяя уникальность нового имени.
        """
        new_name = obj_in.name
        if new_name and new_name != db_obj.name:
            result = await db.execute(
                select(CharityProject).where(
                    CharityProject.name == new_name
                )
            )
            existing_project = result.scalar_one_or_none()
            if existing_project:
                raise HTTPException(
                    status_code=400,
                    detail="Проект с таким именем уже существует."
                )

        return await super().update(db, db_obj, obj_in)


crud_charity_project = CRUDCharityProject(CharityProject)

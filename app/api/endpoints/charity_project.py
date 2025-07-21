from datetime import datetime
from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.validators import (
    check_full_amount_not_less_than_invested,
    check_project_can_be_deleted,
    check_project_exists,
    check_project_not_fully_invested,
)
from app.core.db import get_async_session
from app.core.dependencies import current_superuser
from app.crud.charity_project import crud_charity_project
from app.models import User
from app.schemas.charity_project import (
    CharityProjectCreate,
    CharityProjectDB,
    CharityProjectUpdate,
)
from app.services.investment import invest_money

router = APIRouter()


@router.get(
    '/',
    response_model=List[CharityProjectDB],
    response_model_exclude_none=True
)
async def get_all_projects(
    session: AsyncSession = Depends(get_async_session)
):
    """Получить все проекты."""
    return await crud_charity_project.get_multi(session)


@router.post(
    '/',
    response_model=CharityProjectDB,
    response_model_exclude_none=True
)
async def create_new_project(
    project_in: CharityProjectCreate,
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_superuser)
):
    """Создать проект и вложить доступные пожертвования."""
    new_project = await crud_charity_project.create(session, project_in)
    await session.refresh(new_project)

    from app.models import Donation
    from sqlalchemy import select

    result = await session.execute(
        select(Donation)
        .where(Donation.fully_invested.is_(False))
        .order_by(Donation.create_date)
    )
    open_donations = result.scalars().all()

    changed_objs = invest_money(target=new_project, sources=open_donations)

    for obj in changed_objs:
        session.add(obj)

    await session.commit()
    await session.refresh(new_project)
    return new_project


@router.patch(
    '/{project_id}',
    response_model=CharityProjectDB,
    response_model_exclude_none=True
)
async def partially_update_project(
    project_id: int,
    project_in: CharityProjectUpdate,
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_superuser)
):
    """Частично обновить проект."""
    db_project = await crud_charity_project.get(session, project_id)
    check_project_exists(db_project)
    check_project_not_fully_invested(db_project)
    check_full_amount_not_less_than_invested(
        project_in.full_amount, db_project.invested_amount
    )

    project = await crud_charity_project.update(
        db=session,
        db_obj=db_project,
        obj_in=project_in
    )

    if project.full_amount == project.invested_amount:
        project.fully_invested = True
        project.close_date = datetime.utcnow()
        await session.commit()
        await session.refresh(project)

    return project


@router.delete(
    '/{project_id}',
    response_model=CharityProjectDB
)
async def delete_project(
    project_id: int,
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_superuser)
):
    """Удалить проект."""
    project = await crud_charity_project.get(db=session, id=project_id)
    check_project_exists(project)
    check_project_can_be_deleted(project)
    return await crud_charity_project.remove(db=session, id=project_id)

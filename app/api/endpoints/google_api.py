from aiogoogle import Aiogoogle
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.validators import handle_google_api_errors
from app.core.db import get_async_session
from app.core.google_client import get_service
from app.core.user import current_superuser
from app.crud.charity_project import crud_charity_project
from app.services.google_api import (
    set_user_permissions,
    spreadsheets_create,
    spreadsheets_update_value
)

router = APIRouter()


@router.post('/', response_model=dict[str, str],
             dependencies=[Depends(current_superuser)])
async def get_report(
    session: AsyncSession = Depends(get_async_session),
    wrapper_services: Aiogoogle = Depends(get_service)
):
    """Создать таблицу в Google Spreadsheets и получить ссылку на неё."""
    projects = await (
        crud_charity_project.get_projects_by_completion_rate(session)
    )
    spreadsheet_id = await spreadsheets_create(wrapper_services)

    await handle_google_api_errors(
        set_user_permissions,
        spreadsheet_id,
        wrapper_services
    )
    spreadsheet_url = await handle_google_api_errors(
        spreadsheets_update_value,
        spreadsheet_id,
        projects,
        wrapper_services
    )

    return {"spreadsheet_url": spreadsheet_url}

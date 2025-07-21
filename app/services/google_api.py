from datetime import datetime

from aiogoogle import Aiogoogle

from .constants import (
    DATETIME_FORMAT,
    TABLE_INPUT_OPTION,
    TABLE_DIMENSION,
    TABLE_RANGE,
    TABLE_ROW_COUNT,
    TABLE_COLUMN_COUNT,
    TableUpdatePayload,
    SHEETS_API_CONFIG,
    DRIVE_API_CONFIG,
    ACCESS_TYPE,
    ACCESS_ROLE,
    GRANTEE_EMAIL,
    PermissionPayload,
    PERMISSION_RESPONSE_FIELDS,
    TABLE_HEADER,
    SPREADSHEET_CONFIG_TEMPLATE,
    SPREADSHEET_URL_TEMPLATE,
    SPREADSHEET_CONFIG_TEMPLATE,
)


def format_timedelta(tdelta, fmt: str) -> str:
    """Форматирует объект timedelta в строку по заданному шаблону."""
    delta_info = {'days': abs(tdelta.days)}
    delta_info['hours'], remainder = divmod(tdelta.seconds, 3600)
    delta_info['minutes'], delta_info['seconds'] = divmod(remainder, 60)
    return fmt.format(**delta_info)


async def spreadsheets_create(wrapper_services: Aiogoogle) -> tuple[str, str]:
    current_time = datetime.now().strftime(DATETIME_FORMAT)

    service = await wrapper_services.discover(**SHEETS_API_CONFIG)

    spreadsheet_config = SPREADSHEET_CONFIG_TEMPLATE.copy()
    spreadsheet_config['properties']['title'] = f'Отчет от {current_time}'

    response = await wrapper_services.as_service_account(
        service.spreadsheets.create(json=spreadsheet_config)
    )

    spreadsheet_id = response['spreadsheetId']
    spreadsheet_url = SPREADSHEET_URL_TEMPLATE.format(spreadsheet_id)
    return spreadsheet_id, spreadsheet_url


async def set_user_permissions(
    spreadsheetid: str,
    wrapper_services: Aiogoogle
) -> None:
    """Назначает права на таблицу пользователю, указанному в конфиге."""
    permissions_body = PermissionPayload(
        type=ACCESS_TYPE,
        role=ACCESS_ROLE,
        emailAddress=GRANTEE_EMAIL,
    )._asdict()

    service = await wrapper_services.discover(**DRIVE_API_CONFIG)

    await wrapper_services.as_service_account(
        service.permissions.create(
            fileId=spreadsheetid,
            json=permissions_body,
            fields=PERMISSION_RESPONSE_FIELDS,
        )
    )


async def spreadsheets_update_value(
    spreadsheet_id: str,
    projects: list,
    wrapper_services: Aiogoogle
) -> None:
    """Обновляет значения в Google-таблице: добавляет отчёт по проектам."""
    current_time = datetime.now().strftime(DATETIME_FORMAT)

    service = await wrapper_services.discover(**SHEETS_API_CONFIG)

    rows_data = TABLE_HEADER.copy()
    rows_data[0][1] = current_time

    for project in projects:
        duration = project["duration"]
        rows_data.append([
            project["name"],
            format_timedelta(
                duration,
                '{days} days {hours}:{minutes}:{seconds}'
            ),
            project["description"],
        ])

    if len(rows_data) > TABLE_ROW_COUNT:
        raise ValueError("Слишком много строк для созданной таблицы")

    max_columns = max(len(row) for row in rows_data)
    if max_columns > TABLE_COLUMN_COUNT:
        raise ValueError("Слишком много столбцов для созданной таблицы")

    update_payload = TableUpdatePayload(
        majorDimension=TABLE_DIMENSION,
        values=rows_data,
    )._asdict()

    await wrapper_services.as_service_account(
        service.spreadsheets.values.update(
            spreadsheetId=spreadsheet_id,
            range=TABLE_RANGE,
            valueInputOption=TABLE_INPUT_OPTION,
            json=update_payload,
        )
    )

from collections import namedtuple
from app.core.config import settings


# === Формат времени и локаль ===
DATETIME_FORMAT = "%Y/%m/%d %H:%M:%S"
SPREADSHEET_LOCALE = 'ru_RU'

# === Габариты таблицы ===
TABLE_ROW_COUNT = 100
TABLE_COLUMN_COUNT = 3

# === Свойства листа Google Sheets ===
DEFAULT_SHEET_TITLE = 'Страница1'

DEFAULT_SHEET_PROPERTIES = {
    'sheetType': 'GRID',
    'sheetId': 0,
    'title': DEFAULT_SHEET_TITLE
}

DEFAULT_GRID_PROPERTIES = {
    'gridProperties': {
        'rowCount': TABLE_ROW_COUNT,
        'columnCount': TABLE_COLUMN_COUNT
    }
}

SPREADSHEET_CONFIG_TEMPLATE = {
    'properties': {
        'title': '',
        'locale': SPREADSHEET_LOCALE
    },
    'sheets': [{
        'properties': {
            **DEFAULT_SHEET_PROPERTIES,
            **DEFAULT_GRID_PROPERTIES
        }
    }]
}

SPREADSHEET_URL_TEMPLATE = "https://docs.google.com/spreadsheets/d/{}"

# === Конфигурация обновления таблицы ===
TABLE_INPUT_OPTION = 'USER_ENTERED'
TABLE_DIMENSION = 'ROWS'
TABLE_RANGE = 'A1:E30'

TableUpdatePayload = namedtuple(
    'TableUpdatePayload',
    ['majorDimension', 'values']
)

# === Конфигурация API ===
SHEETS_API_CONFIG = {'sheets': 'v4'}
DRIVE_API_CONFIG = {'drive': 'v3'}

# === Права доступа к таблице ===
ACCESS_TYPE = 'user'
ACCESS_ROLE = 'writer'
GRANTEE_EMAIL = settings.email

PermissionPayload = namedtuple(
    'PermissionPayload',
    ['type', 'role', 'emailAddress']
)

PERMISSION_RESPONSE_FIELDS = 'id'

# === Заголовки таблицы по умолчанию ===
TABLE_HEADER = [
    ['Отчет от', 'дата'],
    ['Топ проектов по скорости закрытия'],
    ['Название проекта', 'Время сбора', 'Описание']
]

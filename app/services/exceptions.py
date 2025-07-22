"""Модуль исключений для работы с таблицами."""


class SpreadsheetStructureError(Exception):
    """Базовое исключение для ошибок структуры таблицы."""


class TooManyRowsError(SpreadsheetStructureError):
    """Слишком много строк для таблицы."""


class TooManyColumnsError(SpreadsheetStructureError):
    """Слишком много столбцов для таблицы."""

from http import HTTPStatus

from fastapi import HTTPException

from app.models import CharityProject


def check_project_exists(project: CharityProject):
    """Проверяет, что проект существует."""
    if not project:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail="Проект не найден"
        )


def check_project_not_fully_invested(project: CharityProject):
    """Проверяет, что проект не полностью проинвестирован."""
    if project.fully_invested:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail=(
                "Нельзя редактировать полностью "
                "проинвестированный проект."
            )
        )


def check_full_amount_not_less_than_invested(
    new_amount: int, invested_amount: int
):
    """Проверяет, что новая сумма не меньше инвестированной."""
    if new_amount is not None and new_amount < invested_amount:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail=(
                "Новая требуемая сумма не может быть "
                "меньше уже инвестированной."
            )
        )


def check_project_can_be_deleted(project: CharityProject):
    """Проверяет, что проект можно удалить."""
    if project.invested_amount > 0:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail=(
                "Нельзя удалить проект, в который уже "
                "были инвестированы средства"
            )
        )

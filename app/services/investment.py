from datetime import datetime


def close_entity(obj) -> None:
    """Закрывает объект, помечая его как полностью инвестированный."""
    obj.fully_invested = True
    obj.close_date = datetime.now()


def invest_money(target, sources: list):
    """
    Инвестирует деньги из источников в целевой объект.

    Возвращает список изменённых объектов.
    """
    changed_objects = []

    for source in sources:
        need = source.full_amount - source.invested_amount
        available = target.full_amount - target.invested_amount

        to_invest = min(need, available)

        source.invested_amount += to_invest
        target.invested_amount += to_invest

        if source.invested_amount == source.full_amount:
            close_entity(source)

        if target.invested_amount == target.full_amount:
            close_entity(target)
            changed_objects.append(source)
            break

        changed_objects.append(source)

    changed_objects.append(target)
    return changed_objects

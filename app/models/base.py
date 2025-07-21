from datetime import datetime
from sqlalchemy import Column, DateTime, Boolean, Integer, CheckConstraint

from app.core.db import Base

DEFAULT_INVESTED_AMOUNT = 0


class BaseDonationProject(Base):
    """
    Абстрактная базовая модель для проектов и пожертвований с инвестированием.
    """
    __abstract__ = True

    invested_amount = Column(Integer, default=DEFAULT_INVESTED_AMOUNT)
    full_amount = Column(Integer, nullable=False)
    fully_invested = Column(Boolean, default=False)
    create_date = Column(DateTime, default=datetime.now)
    close_date = Column(DateTime, default=None)

    __table_args__ = (
        CheckConstraint(
            'full_amount > 0', name='check_full_amount_positive'
        ),
        CheckConstraint(
            'invested_amount <= full_amount', name='check_invested_not_exceed'
        ),
    )

from sqlalchemy import Column, String, Text

from app.models.base import BaseDonationProject


class CharityProject(BaseDonationProject):
    """
    Модель благотворительного проекта с уникальным именем и описанием.
    """
    __tablename__ = 'charityproject'

    name = Column(String(100), unique=True, nullable=False)
    description = Column(Text, nullable=False)

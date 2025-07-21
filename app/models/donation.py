from sqlalchemy import Column, ForeignKey, Integer, Text

from app.models.base import BaseDonationProject


class Donation(BaseDonationProject):
    """
    Модель пожертвования с привязкой к пользователю и комментарием.
    """
    __tablename__ = 'donation'

    user_id = Column(Integer, ForeignKey('user.id'))
    comment = Column(Text, nullable=True)

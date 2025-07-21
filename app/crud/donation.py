from typing import List

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.models.charity_project import CharityProject
from app.models.donation import Donation
from app.models.user import User
from app.schemas.donation import DonationCreate, DonationUpdate
from app.services.investment import invest_money


class DonationCRUD(CRUDBase[Donation, DonationCreate, DonationUpdate]):
    """
    CRUD для пожертвований с логикой инвестирования.
    """

    async def create_donation(
        self,
        donation_in: DonationCreate,
        session: AsyncSession,
        user: User,
    ) -> Donation:
        """
        Создает пожертвование и инвестирует его.
        """
        new_donation = Donation(**donation_in.dict(), user_id=user.id)
        session.add(new_donation)
        await session.commit()
        await session.refresh(new_donation)

        result = await session.execute(
            select(CharityProject)
            .where(CharityProject.fully_invested.is_(False))
            .order_by(CharityProject.create_date)
        )
        open_projects = result.scalars().all()

        changed_objs = invest_money(target=new_donation, sources=open_projects)

        for obj in changed_objs:
            session.add(obj)

        await session.commit()
        await session.refresh(new_donation)
        return new_donation

    async def get_user_donations(
        self,
        session: AsyncSession,
        user: User
    ) -> List[Donation]:
        """
        Возвращает пожертвования пользователя.
        """
        result = await session.execute(
            select(Donation).where(Donation.user_id == user.id)
        )
        return result.scalars().all()

    async def get_all_donations(
        self,
        session: AsyncSession
    ) -> List[Donation]:
        """
        Возвращает все пожертвования.
        """
        result = await session.execute(
            select(Donation).order_by(Donation.create_date)
        )
        return result.scalars().all()


donation_crud = DonationCRUD(Donation)

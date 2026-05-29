from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select

from app.models.commodity import Commodity


class CommodityRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, commodity: Commodity) -> Commodity:
        self.session.add(commodity)
        await self.session.commit()
        await self.session.refresh(commodity)
        return commodity

    async def list(self, active_only: bool = False) -> list[Commodity]:
        statement = select(Commodity).order_by(Commodity.name)
        if active_only:
            statement = statement.where(Commodity.active.is_(True))
        result = await self.session.execute(statement)
        return list(result.scalars().all())

    async def get(self, commodity_id: int) -> Commodity | None:
        return await self.session.get(Commodity, commodity_id)

    async def get_by_symbol(self, symbol: str) -> Commodity | None:
        result = await self.session.execute(select(Commodity).where(Commodity.symbol == symbol))
        return result.scalar_one_or_none()

    async def update(self, commodity: Commodity, values: dict) -> Commodity:
        for key, value in values.items():
            setattr(commodity, key, value)
        self.session.add(commodity)
        await self.session.commit()
        await self.session.refresh(commodity)
        return commodity

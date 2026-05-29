from __future__ import annotations

from datetime import date

from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select

from app.models.market_price import MarketPrice


class MarketPriceRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, price: MarketPrice) -> MarketPrice:
        self.session.add(price)
        await self.session.commit()
        await self.session.refresh(price)
        return price

    async def list(self, commodity_id: int | None = None) -> list[MarketPrice]:
        statement = select(MarketPrice).order_by(MarketPrice.reference_date.desc())
        if commodity_id:
            statement = statement.where(MarketPrice.commodity_id == commodity_id)
        result = await self.session.execute(statement)
        return list(result.scalars().all())

    async def list_between(self, commodity_id: int, start_date: date | None, end_date: date | None) -> list[MarketPrice]:
        statement = select(MarketPrice).where(MarketPrice.commodity_id == commodity_id)
        if start_date:
            statement = statement.where(MarketPrice.reference_date >= start_date)
        if end_date:
            statement = statement.where(MarketPrice.reference_date <= end_date)
        statement = statement.order_by(MarketPrice.reference_date)
        result = await self.session.execute(statement)
        return list(result.scalars().all())

    async def latest_for_commodity(self, commodity_id: int, on_or_before: date | None = None) -> MarketPrice | None:
        statement = select(MarketPrice).where(MarketPrice.commodity_id == commodity_id)
        if on_or_before:
            statement = statement.where(MarketPrice.reference_date <= on_or_before)
        statement = statement.order_by(MarketPrice.reference_date.desc()).limit(1)
        result = await self.session.execute(statement)
        return result.scalar_one_or_none()

    async def previous_for_commodity(self, commodity_id: int, reference_date: date) -> MarketPrice | None:
        statement = (
            select(MarketPrice)
            .where(MarketPrice.commodity_id == commodity_id, MarketPrice.reference_date < reference_date)
            .order_by(MarketPrice.reference_date.desc())
            .limit(1)
        )
        result = await self.session.execute(statement)
        return result.scalar_one_or_none()

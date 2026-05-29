from __future__ import annotations

from datetime import date

from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.market_price import MarketPrice
from app.repositories.commodity_repository import CommodityRepository
from app.repositories.market_price_repository import MarketPriceRepository
from app.schemas.market_price import MarketPriceCreate
from app.services.calculation_service import calculate_price_variation


class MarketPriceService:
    def __init__(self, session: AsyncSession):
        self.repository = MarketPriceRepository(session)
        self.commodity_repository = CommodityRepository(session)

    async def create(self, payload: MarketPriceCreate) -> MarketPrice:
        commodity = await self.commodity_repository.get(payload.commodity_id)
        if not commodity:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Commodity not found")
        previous = await self.repository.previous_for_commodity(payload.commodity_id, payload.reference_date)
        variation = calculate_price_variation(previous.price if previous else None, payload.price)
        price = MarketPrice(**payload.model_dump(), variation_percent=variation)
        return await self.repository.create(price)

    async def list(self, commodity_id: int | None = None) -> list[MarketPrice]:
        return await self.repository.list(commodity_id=commodity_id)

    async def history(self, commodity_id: int, start_date: date | None = None, end_date: date | None = None) -> list[MarketPrice]:
        commodity = await self.commodity_repository.get(commodity_id)
        if not commodity:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Commodity not found")
        return await self.repository.list_between(commodity_id, start_date, end_date)

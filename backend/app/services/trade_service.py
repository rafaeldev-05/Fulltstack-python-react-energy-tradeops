from fastapi import HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.enums import OperationType, TradeStatus
from app.models.trade_operation import TradeOperation
from app.repositories.commodity_repository import CommodityRepository
from app.repositories.market_price_repository import MarketPriceRepository
from app.repositories.trade_repository import TradeRepository
from app.schemas.trade_operation import TradeOperationCreate, TradeOperationDetail, TradeOperationUpdate
from app.services.calculation_service import (
    calculate_estimated_margin,
    calculate_trade_exposure,
    calculate_trade_total,
)


class TradeService:
    def __init__(self, session: AsyncSession):
        self.repository = TradeRepository(session)
        self.commodity_repository = CommodityRepository(session)
        self.market_price_repository = MarketPriceRepository(session)

    async def create(self, payload: TradeOperationCreate) -> TradeOperation:
        commodity = await self.commodity_repository.get(payload.commodity_id)
        if not commodity:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Commodity not found")
        if payload.settlement_date < payload.trade_date:
            raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Settlement date cannot be before trade date")
        trade = TradeOperation(**payload.model_dump())
        try:
            return await self.repository.create(trade)
        except IntegrityError as exc:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Trade code already exists") from exc

    async def list(
        self,
        commodity_id: int | None = None,
        region: str | None = None,
        status_filter: TradeStatus | None = None,
        operation_type: OperationType | None = None,
    ) -> list[TradeOperationDetail]:
        trades = await self.repository.list(commodity_id, region, status_filter, operation_type)
        return [await self.to_detail(trade) for trade in trades]

    async def get(self, trade_id: int) -> TradeOperation:
        trade = await self.repository.get(trade_id)
        if not trade:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Trade operation not found")
        return trade

    async def get_detail(self, trade_id: int) -> TradeOperationDetail:
        return await self.to_detail(await self.get(trade_id))

    async def update(self, trade_id: int, payload: TradeOperationUpdate) -> TradeOperation:
        trade = await self.get(trade_id)
        values = payload.model_dump(exclude_unset=True)
        if trade.status == TradeStatus.SETTLED and values:
            protected = {"volume", "unit_price", "operation_type", "commodity_id", "trade_date", "settlement_date"}
            if protected.intersection(values):
                raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Settled trades cannot have economic terms changed")
        try:
            return await self.repository.update(trade, values)
        except IntegrityError as exc:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Trade code already exists") from exc

    async def confirm(self, trade_id: int) -> TradeOperation:
        trade = await self.get(trade_id)
        if trade.status not in {TradeStatus.DRAFT, TradeStatus.CONFIRMED}:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Only draft trades can be confirmed")
        return await self.repository.update(trade, {"status": TradeStatus.CONFIRMED})

    async def settle(self, trade_id: int) -> TradeOperation:
        trade = await self.get(trade_id)
        if trade.status == TradeStatus.CANCELLED:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Cancelled trades cannot be settled")
        return await self.repository.update(trade, {"status": TradeStatus.SETTLED})

    async def cancel(self, trade_id: int) -> TradeOperation:
        trade = await self.get(trade_id)
        if trade.status == TradeStatus.SETTLED:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Settled trades cannot be cancelled")
        return await self.repository.update(trade, {"status": TradeStatus.CANCELLED})

    async def to_detail(self, trade: TradeOperation) -> TradeOperationDetail:
        latest_market = await self.market_price_repository.latest_for_commodity(trade.commodity_id, trade.trade_date)
        data = trade.model_dump()
        data.update(
            {
                "total_value": calculate_trade_total(trade),
                "exposure": calculate_trade_exposure(trade),
                "estimated_margin": calculate_estimated_margin(trade, latest_market),
            }
        )
        return TradeOperationDetail(**data)

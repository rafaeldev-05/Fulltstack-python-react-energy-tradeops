from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select

from app.models.enums import OperationType, TradeStatus
from app.models.trade_operation import TradeOperation


class TradeRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, trade: TradeOperation) -> TradeOperation:
        self.session.add(trade)
        await self.session.commit()
        await self.session.refresh(trade)
        return trade

    async def list(
        self,
        commodity_id: int | None = None,
        region: str | None = None,
        status: TradeStatus | None = None,
        operation_type: OperationType | None = None,
    ) -> list[TradeOperation]:
        statement = select(TradeOperation).order_by(TradeOperation.trade_date.desc())
        if commodity_id:
            statement = statement.where(TradeOperation.commodity_id == commodity_id)
        if region:
            statement = statement.where(TradeOperation.region == region)
        if status:
            statement = statement.where(TradeOperation.status == status)
        if operation_type:
            statement = statement.where(TradeOperation.operation_type == operation_type)
        result = await self.session.execute(statement)
        return list(result.scalars().all())

    async def get(self, trade_id: int) -> TradeOperation | None:
        return await self.session.get(TradeOperation, trade_id)

    async def update(self, trade: TradeOperation, values: dict) -> TradeOperation:
        for key, value in values.items():
            setattr(trade, key, value)
        self.session.add(trade)
        await self.session.commit()
        await self.session.refresh(trade)
        return trade

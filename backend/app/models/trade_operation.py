from datetime import date, datetime, timezone

from sqlmodel import Field, SQLModel

from app.models.enums import OperationType, TradeStatus


class TradeOperation(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    trade_code: str = Field(index=True, unique=True, max_length=40)
    operation_type: OperationType = Field(index=True)
    commodity_id: int = Field(foreign_key="commodity.id", index=True)
    volume: float = Field(gt=0)
    unit_price: float = Field(gt=0)
    currency: str = Field(default="USD", max_length=3)
    region: str = Field(index=True, max_length=80)
    counterparty: str = Field(index=True, max_length=120)
    trade_date: date = Field(index=True)
    settlement_date: date
    status: TradeStatus = Field(default=TradeStatus.DRAFT, index=True)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc), index=True)

from datetime import date, datetime

from pydantic import BaseModel, ConfigDict, Field

from app.models.enums import OperationType, TradeStatus


class TradeOperationBase(BaseModel):
    trade_code: str = Field(min_length=4, max_length=40)
    operation_type: OperationType
    commodity_id: int
    volume: float = Field(gt=0)
    unit_price: float = Field(gt=0)
    currency: str = Field(default="USD", min_length=3, max_length=3)
    region: str = Field(max_length=80)
    counterparty: str = Field(max_length=120)
    trade_date: date
    settlement_date: date


class TradeOperationCreate(TradeOperationBase):
    pass


class TradeOperationUpdate(BaseModel):
    trade_code: str | None = Field(default=None, min_length=4, max_length=40)
    operation_type: OperationType | None = None
    commodity_id: int | None = None
    volume: float | None = Field(default=None, gt=0)
    unit_price: float | None = Field(default=None, gt=0)
    currency: str | None = Field(default=None, min_length=3, max_length=3)
    region: str | None = Field(default=None, max_length=80)
    counterparty: str | None = Field(default=None, max_length=120)
    trade_date: date | None = None
    settlement_date: date | None = None
    status: TradeStatus | None = None


class TradeOperationRead(TradeOperationBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    status: TradeStatus
    created_at: datetime


class TradeOperationDetail(TradeOperationRead):
    total_value: float
    exposure: float
    estimated_margin: float | None = None

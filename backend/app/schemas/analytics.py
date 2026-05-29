from pydantic import BaseModel


class SummaryResponse(BaseModel):
    total_operations: int
    total_traded_volume: float
    total_financial_exposure: float
    average_estimated_margin: float
    open_operations: int
    delayed_shipments: int
    critical_alerts: int
    top_counterparties: list[dict]


class MarginAnalysisItem(BaseModel):
    commodity_id: int
    commodity: str
    average_margin: float
    negative_trades: int


class VolatilityItem(BaseModel):
    commodity_id: int
    commodity: str
    volatility_percent: float

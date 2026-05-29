from datetime import datetime

from pydantic import BaseModel, ConfigDict

from app.models.enums import RiskSeverity


class RiskAlertCreate(BaseModel):
    title: str
    description: str
    severity: RiskSeverity
    related_trade_id: int | None = None


class RiskAlertRead(RiskAlertCreate):
    model_config = ConfigDict(from_attributes=True)

    id: int
    created_at: datetime
    resolved: bool

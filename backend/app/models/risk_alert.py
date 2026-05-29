from datetime import datetime, timezone

from sqlmodel import Field, SQLModel

from app.models.enums import RiskSeverity


class RiskAlert(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    title: str = Field(index=True, max_length=160)
    description: str
    severity: RiskSeverity = Field(index=True)
    related_trade_id: int | None = Field(default=None, foreign_key="tradeoperation.id", index=True)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc), index=True)
    resolved: bool = Field(default=False, index=True)

from datetime import date

from sqlmodel import Field, SQLModel


class MarketPrice(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    commodity_id: int = Field(foreign_key="commodity.id", index=True)
    reference_date: date = Field(index=True)
    price: float = Field(gt=0)
    currency: str = Field(default="USD", max_length=3)
    source: str = Field(default="SIMULATED", max_length=80)
    variation_percent: float = Field(default=0)

from datetime import date

from pydantic import BaseModel, ConfigDict, Field


class MarketPriceBase(BaseModel):
    commodity_id: int
    reference_date: date
    price: float = Field(gt=0)
    currency: str = Field(default="USD", min_length=3, max_length=3)
    source: str = "SIMULATED"


class MarketPriceCreate(MarketPriceBase):
    pass


class MarketPriceRead(MarketPriceBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    variation_percent: float

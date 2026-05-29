from pydantic import BaseModel, ConfigDict, Field


class CommodityBase(BaseModel):
    name: str = Field(min_length=2, max_length=120)
    symbol: str = Field(min_length=2, max_length=20)
    category: str = Field(max_length=80)
    unit: str = Field(max_length=40)
    active: bool = True


class CommodityCreate(CommodityBase):
    pass


class CommodityUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=2, max_length=120)
    symbol: str | None = Field(default=None, min_length=2, max_length=20)
    category: str | None = Field(default=None, max_length=80)
    unit: str | None = Field(default=None, max_length=40)
    active: bool | None = None


class CommodityRead(CommodityBase):
    model_config = ConfigDict(from_attributes=True)

    id: int

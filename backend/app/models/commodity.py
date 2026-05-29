from sqlmodel import Field, SQLModel


class Commodity(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(index=True, min_length=2, max_length=120)
    symbol: str = Field(index=True, min_length=2, max_length=20, unique=True)
    category: str = Field(index=True, max_length=80)
    unit: str = Field(max_length=40)
    active: bool = Field(default=True, index=True)

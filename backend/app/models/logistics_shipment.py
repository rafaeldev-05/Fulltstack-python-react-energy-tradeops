from datetime import date

from sqlmodel import Field, SQLModel

from app.models.enums import ShipmentStatus, TransportMode


class LogisticsShipment(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    trade_operation_id: int = Field(foreign_key="tradeoperation.id", index=True)
    origin: str = Field(max_length=120)
    destination: str = Field(max_length=120)
    transport_mode: TransportMode = Field(index=True)
    estimated_departure: date
    estimated_arrival: date = Field(index=True)
    actual_arrival: date | None = None
    status: ShipmentStatus = Field(default=ShipmentStatus.PLANNED, index=True)

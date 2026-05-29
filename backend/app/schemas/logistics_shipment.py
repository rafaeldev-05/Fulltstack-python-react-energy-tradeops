from datetime import date

from pydantic import BaseModel, ConfigDict

from app.models.enums import ShipmentStatus, TransportMode


class LogisticsShipmentBase(BaseModel):
    trade_operation_id: int
    origin: str
    destination: str
    transport_mode: TransportMode
    estimated_departure: date
    estimated_arrival: date
    actual_arrival: date | None = None


class LogisticsShipmentCreate(LogisticsShipmentBase):
    pass


class LogisticsShipmentUpdate(BaseModel):
    trade_operation_id: int | None = None
    origin: str | None = None
    destination: str | None = None
    transport_mode: TransportMode | None = None
    estimated_departure: date | None = None
    estimated_arrival: date | None = None
    actual_arrival: date | None = None
    status: ShipmentStatus | None = None


class LogisticsShipmentRead(LogisticsShipmentBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    status: ShipmentStatus
    delay_days: int

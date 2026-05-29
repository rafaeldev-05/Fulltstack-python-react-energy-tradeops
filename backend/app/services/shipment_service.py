from datetime import date

from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.enums import ShipmentStatus, TradeStatus
from app.models.logistics_shipment import LogisticsShipment
from app.repositories.shipment_repository import ShipmentRepository
from app.repositories.trade_repository import TradeRepository
from app.schemas.logistics_shipment import LogisticsShipmentCreate, LogisticsShipmentRead, LogisticsShipmentUpdate
from app.services.calculation_service import calculate_delay_days


class ShipmentService:
    def __init__(self, session: AsyncSession):
        self.repository = ShipmentRepository(session)
        self.trade_repository = TradeRepository(session)

    async def create(self, payload: LogisticsShipmentCreate) -> LogisticsShipment:
        trade = await self.trade_repository.get(payload.trade_operation_id)
        if not trade:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Trade operation not found")
        if trade.status == TradeStatus.CANCELLED:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Cannot create shipment for cancelled trade")
        if payload.estimated_arrival < payload.estimated_departure:
            raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Estimated arrival cannot be before departure")
        shipment = LogisticsShipment(**payload.model_dump())
        return await self.repository.create(shipment)

    async def list(self, status_filter: ShipmentStatus | None = None) -> list[LogisticsShipmentRead]:
        shipments = await self.repository.list(status_filter)
        return [self.to_read(shipment) for shipment in shipments]

    async def get(self, shipment_id: int) -> LogisticsShipment:
        shipment = await self.repository.get(shipment_id)
        if not shipment:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Shipment not found")
        return shipment

    async def get_read(self, shipment_id: int) -> LogisticsShipmentRead:
        return self.to_read(await self.get(shipment_id))

    async def update(self, shipment_id: int, payload: LogisticsShipmentUpdate) -> LogisticsShipment:
        shipment = await self.get(shipment_id)
        values = payload.model_dump(exclude_unset=True)
        return await self.repository.update(shipment, values)

    async def mark_delayed(self, shipment_id: int) -> LogisticsShipment:
        shipment = await self.get(shipment_id)
        if shipment.status in {ShipmentStatus.DELIVERED, ShipmentStatus.CANCELLED}:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Delivered or cancelled shipments cannot be delayed")
        return await self.repository.update(shipment, {"status": ShipmentStatus.DELAYED})

    async def mark_delivered(self, shipment_id: int, actual_arrival: date | None = None) -> LogisticsShipment:
        shipment = await self.get(shipment_id)
        if shipment.status == ShipmentStatus.CANCELLED:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Cancelled shipments cannot be delivered")
        return await self.repository.update(
            shipment,
            {"status": ShipmentStatus.DELIVERED, "actual_arrival": actual_arrival or date.today()},
        )

    def to_read(self, shipment: LogisticsShipment) -> LogisticsShipmentRead:
        data = shipment.model_dump()
        data["delay_days"] = calculate_delay_days(shipment)
        return LogisticsShipmentRead(**data)

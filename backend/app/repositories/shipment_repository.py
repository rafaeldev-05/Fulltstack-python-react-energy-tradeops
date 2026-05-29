from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select

from app.models.enums import ShipmentStatus
from app.models.logistics_shipment import LogisticsShipment


class ShipmentRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, shipment: LogisticsShipment) -> LogisticsShipment:
        self.session.add(shipment)
        await self.session.commit()
        await self.session.refresh(shipment)
        return shipment

    async def list(self, status: ShipmentStatus | None = None) -> list[LogisticsShipment]:
        statement = select(LogisticsShipment).order_by(LogisticsShipment.estimated_arrival.desc())
        if status:
            statement = statement.where(LogisticsShipment.status == status)
        result = await self.session.execute(statement)
        return list(result.scalars().all())

    async def get(self, shipment_id: int) -> LogisticsShipment | None:
        return await self.session.get(LogisticsShipment, shipment_id)

    async def update(self, shipment: LogisticsShipment, values: dict) -> LogisticsShipment:
        for key, value in values.items():
            setattr(shipment, key, value)
        self.session.add(shipment)
        await self.session.commit()
        await self.session.refresh(shipment)
        return shipment

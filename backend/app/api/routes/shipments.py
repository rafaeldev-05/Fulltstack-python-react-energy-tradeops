from datetime import date

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.session import get_session
from app.models.enums import ShipmentStatus
from app.schemas.logistics_shipment import LogisticsShipmentCreate, LogisticsShipmentRead, LogisticsShipmentUpdate
from app.services.shipment_service import ShipmentService

router = APIRouter(prefix="/shipments", tags=["Logistics"])


@router.post("", response_model=LogisticsShipmentRead, status_code=201)
async def create_shipment(payload: LogisticsShipmentCreate, session: AsyncSession = Depends(get_session)):
    shipment = await ShipmentService(session).create(payload)
    return ShipmentService(session).to_read(shipment)


@router.get("", response_model=list[LogisticsShipmentRead])
async def list_shipments(status: ShipmentStatus | None = None, session: AsyncSession = Depends(get_session)):
    return await ShipmentService(session).list(status)


@router.get("/{shipment_id}", response_model=LogisticsShipmentRead)
async def get_shipment(shipment_id: int, session: AsyncSession = Depends(get_session)):
    return await ShipmentService(session).get_read(shipment_id)


@router.patch("/{shipment_id}", response_model=LogisticsShipmentRead)
async def update_shipment(shipment_id: int, payload: LogisticsShipmentUpdate, session: AsyncSession = Depends(get_session)):
    service = ShipmentService(session)
    shipment = await service.update(shipment_id, payload)
    return service.to_read(shipment)


@router.patch("/{shipment_id}/mark-delivered", response_model=LogisticsShipmentRead)
async def mark_shipment_delivered(
    shipment_id: int,
    actual_arrival: date | None = None,
    session: AsyncSession = Depends(get_session),
):
    service = ShipmentService(session)
    shipment = await service.mark_delivered(shipment_id, actual_arrival)
    return service.to_read(shipment)


@router.patch("/{shipment_id}/mark-delayed", response_model=LogisticsShipmentRead)
async def mark_shipment_delayed(shipment_id: int, session: AsyncSession = Depends(get_session)):
    service = ShipmentService(session)
    shipment = await service.mark_delayed(shipment_id)
    return service.to_read(shipment)

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.session import get_session
from app.schemas.commodity import CommodityCreate, CommodityRead, CommodityUpdate
from app.services.commodity_service import CommodityService

router = APIRouter(prefix="/commodities", tags=["Commodities"])


@router.post("", response_model=CommodityRead, status_code=201)
async def create_commodity(payload: CommodityCreate, session: AsyncSession = Depends(get_session)):
    return await CommodityService(session).create(payload)


@router.get("", response_model=list[CommodityRead])
async def list_commodities(active_only: bool = False, session: AsyncSession = Depends(get_session)):
    return await CommodityService(session).list(active_only=active_only)


@router.get("/{commodity_id}", response_model=CommodityRead)
async def get_commodity(commodity_id: int, session: AsyncSession = Depends(get_session)):
    return await CommodityService(session).get(commodity_id)


@router.patch("/{commodity_id}", response_model=CommodityRead)
async def update_commodity(commodity_id: int, payload: CommodityUpdate, session: AsyncSession = Depends(get_session)):
    return await CommodityService(session).update(commodity_id, payload)

from datetime import date

from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.session import get_session
from app.schemas.market_price import MarketPriceCreate, MarketPriceRead
from app.services.market_price_service import MarketPriceService

router = APIRouter(prefix="/market-prices", tags=["Market Prices"])


@router.post("", response_model=MarketPriceRead, status_code=201)
async def create_market_price(payload: MarketPriceCreate, session: AsyncSession = Depends(get_session)):
    return await MarketPriceService(session).create(payload)


@router.get("", response_model=list[MarketPriceRead])
async def list_market_prices(commodity_id: int | None = None, session: AsyncSession = Depends(get_session)):
    return await MarketPriceService(session).list(commodity_id=commodity_id)


@router.get("/{commodity_id}", response_model=list[MarketPriceRead])
async def get_market_price_history(
    commodity_id: int,
    start_date: date | None = Query(default=None),
    end_date: date | None = Query(default=None),
    session: AsyncSession = Depends(get_session),
):
    return await MarketPriceService(session).history(commodity_id, start_date, end_date)

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.session import get_session
from app.schemas.analytics import MarginAnalysisItem, SummaryResponse, VolatilityItem
from app.services.analytics_service import AnalyticsService

router = APIRouter(prefix="/analytics", tags=["Analytics"])


@router.get("/summary", response_model=SummaryResponse)
async def get_summary(session: AsyncSession = Depends(get_session)):
    return await AnalyticsService(session).summary()


@router.get("/exposure-by-region")
async def get_exposure_by_region(session: AsyncSession = Depends(get_session)):
    return await AnalyticsService(session).exposure_by_region()


@router.get("/volume-by-commodity")
async def get_volume_by_commodity(session: AsyncSession = Depends(get_session)):
    return await AnalyticsService(session).volume_by_commodity()


@router.get("/trades-by-status")
async def get_trades_by_status(session: AsyncSession = Depends(get_session)):
    return await AnalyticsService(session).trades_by_status()


@router.get("/margin-analysis", response_model=list[MarginAnalysisItem])
async def get_margin_analysis(session: AsyncSession = Depends(get_session)):
    return await AnalyticsService(session).margin_analysis()


@router.get("/volatility", response_model=list[VolatilityItem])
async def get_volatility(days: int = 30, session: AsyncSession = Depends(get_session)):
    return await AnalyticsService(session).volatility(days)


@router.get("/delayed-shipments")
async def get_delayed_shipments(session: AsyncSession = Depends(get_session)):
    return await AnalyticsService(session).delayed_shipments()

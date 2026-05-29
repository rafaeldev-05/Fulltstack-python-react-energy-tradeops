import asyncio
from contextlib import asynccontextmanager, suppress

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes import analytics, commodities, market_prices, risk_alerts, shipments, trades
from app.core.config import get_settings
from app.database.session import AsyncSessionLocal, init_db
from app.models import Commodity, LogisticsShipment, MarketPrice, RiskAlert, TradeOperation
from app.utils.seed import seed_database
from app.workers.risk_monitor import risk_monitor_loop, run_once

_ = (Commodity, MarketPrice, TradeOperation, LogisticsShipment, RiskAlert)


@asynccontextmanager
async def lifespan(app: FastAPI):
    settings = get_settings()
    await init_db()
    async with AsyncSessionLocal() as session:
        if settings.seed_on_startup:
            await seed_database(session)
    await run_once()
    monitor_task = None
    if settings.risk_monitor_enabled:
        monitor_task = asyncio.create_task(risk_monitor_loop())
    yield
    if monitor_task:
        monitor_task.cancel()
        with suppress(asyncio.CancelledError):
            await monitor_task


settings = get_settings()
app = FastAPI(
    title=settings.app_name,
    description="Operational trading, logistics analytics and risk-control API for energy commodities.",
    version="1.0.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(commodities.router, prefix=settings.api_prefix)
app.include_router(market_prices.router, prefix=settings.api_prefix)
app.include_router(trades.router, prefix=settings.api_prefix)
app.include_router(shipments.router, prefix=settings.api_prefix)
app.include_router(risk_alerts.router, prefix=settings.api_prefix)
app.include_router(analytics.router, prefix=settings.api_prefix)


@app.get("/health", tags=["System"])
async def health_check():
    return {"status": "ok", "service": settings.app_name}

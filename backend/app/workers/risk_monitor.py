import asyncio
from contextlib import suppress

from app.core.config import get_settings
from app.database.session import AsyncSessionLocal
from app.services.risk_service import RiskService


async def run_once() -> dict:
    async with AsyncSessionLocal() as session:
        return await RiskService(session).run_monitoring_cycle()


async def risk_monitor_loop() -> None:
    settings = get_settings()
    await asyncio.sleep(2)
    while True:
        with suppress(Exception):
            await run_once()
        await asyncio.sleep(settings.risk_monitor_interval_seconds)

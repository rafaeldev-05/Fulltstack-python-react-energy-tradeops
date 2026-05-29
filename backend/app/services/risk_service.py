from datetime import date, timedelta

from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import get_settings
from app.models.enums import RiskSeverity, ShipmentStatus
from app.models.risk_alert import RiskAlert
from app.repositories.commodity_repository import CommodityRepository
from app.repositories.market_price_repository import MarketPriceRepository
from app.repositories.risk_alert_repository import RiskAlertRepository
from app.repositories.shipment_repository import ShipmentRepository
from app.repositories.trade_repository import TradeRepository
from app.schemas.risk_alert import RiskAlertCreate
from app.services.calculation_service import calculate_delay_days, calculate_estimated_margin, calculate_simple_volatility


class RiskService:
    def __init__(self, session: AsyncSession):
        self.session = session
        self.settings = get_settings()
        self.repository = RiskAlertRepository(session)
        self.trade_repository = TradeRepository(session)
        self.market_price_repository = MarketPriceRepository(session)
        self.shipment_repository = ShipmentRepository(session)
        self.commodity_repository = CommodityRepository(session)

    async def create(self, payload: RiskAlertCreate) -> RiskAlert:
        return await self.repository.create(RiskAlert(**payload.model_dump()))

    async def list(self, severity: RiskSeverity | None = None, resolved: bool | None = None) -> list[RiskAlert]:
        return await self.repository.list(severity, resolved)

    async def resolve(self, alert_id: int) -> RiskAlert:
        alert = await self.repository.get(alert_id)
        if not alert:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Risk alert not found")
        return await self.repository.resolve(alert)

    async def run_monitoring_cycle(self) -> dict:
        existing = await self.repository.list(resolved=False)
        fingerprints = {self._fingerprint(alert.title, alert.related_trade_id) for alert in existing}
        created = 0
        created += await self._check_negative_margins(fingerprints)
        created += await self._check_delayed_shipments(fingerprints)
        created += await self._check_high_volatility(fingerprints)
        return {"alerts_created": created}

    async def _check_negative_margins(self, fingerprints: set[str]) -> int:
        created = 0
        trades = await self.trade_repository.list()
        for trade in trades:
            market_price = await self.market_price_repository.latest_for_commodity(trade.commodity_id, trade.trade_date)
            margin = calculate_estimated_margin(trade, market_price)
            if margin is None or margin >= self.settings.negative_margin_alert_threshold:
                continue
            title = f"Negative margin above threshold for {trade.trade_code}"
            fingerprint = self._fingerprint(title, trade.id)
            if fingerprint in fingerprints:
                continue
            severity = RiskSeverity.CRITICAL if margin < self.settings.negative_margin_alert_threshold * 3 else RiskSeverity.HIGH
            await self.create(
                RiskAlertCreate(
                    title=title,
                    description=f"Estimated margin is {margin:,.2f} {trade.currency}, breaching configured threshold.",
                    severity=severity,
                    related_trade_id=trade.id,
                )
            )
            fingerprints.add(fingerprint)
            created += 1
        return created

    async def _check_delayed_shipments(self, fingerprints: set[str]) -> int:
        created = 0
        shipments = await self.shipment_repository.list()
        for shipment in shipments:
            delay_days = calculate_delay_days(shipment)
            if delay_days <= 0 or shipment.status in {ShipmentStatus.DELIVERED, ShipmentStatus.CANCELLED}:
                continue
            title = f"Shipment delayed for trade {shipment.trade_operation_id}"
            fingerprint = self._fingerprint(title, shipment.trade_operation_id)
            if fingerprint in fingerprints:
                continue
            severity = RiskSeverity.CRITICAL if delay_days >= 7 else RiskSeverity.HIGH
            await self.create(
                RiskAlertCreate(
                    title=title,
                    description=f"Shipment {shipment.id} is delayed by {delay_days} day(s) on route {shipment.origin} to {shipment.destination}.",
                    severity=severity,
                    related_trade_id=shipment.trade_operation_id,
                )
            )
            fingerprints.add(fingerprint)
            created += 1
        return created

    async def _check_high_volatility(self, fingerprints: set[str]) -> int:
        created = 0
        commodities = await self.commodity_repository.list(active_only=True)
        start_date = date.today() - timedelta(days=30)
        for commodity in commodities:
            prices = await self.market_price_repository.list_between(commodity.id, start_date, date.today())
            volatility = calculate_simple_volatility(prices)
            if volatility < self.settings.high_volatility_threshold_percent:
                continue
            title = f"High volatility detected for {commodity.symbol}"
            fingerprint = self._fingerprint(title, None)
            if fingerprint in fingerprints:
                continue
            await self.create(
                RiskAlertCreate(
                    title=title,
                    description=f"{commodity.name} shows {volatility:.2f}% volatility over the last 30 days.",
                    severity=RiskSeverity.MEDIUM if volatility < 12 else RiskSeverity.HIGH,
                )
            )
            fingerprints.add(fingerprint)
            created += 1
        return created

    @staticmethod
    def _fingerprint(title: str, related_trade_id: int | None) -> str:
        return f"{title}|{related_trade_id or 'none'}"

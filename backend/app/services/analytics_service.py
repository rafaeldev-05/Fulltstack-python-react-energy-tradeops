from collections import Counter, defaultdict
from datetime import date, timedelta

from sqlalchemy.ext.asyncio import AsyncSession

from app.models.enums import RiskSeverity, ShipmentStatus, TradeStatus
from app.repositories.commodity_repository import CommodityRepository
from app.repositories.market_price_repository import MarketPriceRepository
from app.repositories.risk_alert_repository import RiskAlertRepository
from app.repositories.shipment_repository import ShipmentRepository
from app.repositories.trade_repository import TradeRepository
from app.schemas.analytics import MarginAnalysisItem, SummaryResponse, VolatilityItem
from app.services.calculation_service import (
    calculate_delay_days,
    calculate_estimated_margin,
    calculate_simple_volatility,
    calculate_trade_total,
)


class AnalyticsService:
    def __init__(self, session: AsyncSession):
        self.trade_repository = TradeRepository(session)
        self.shipment_repository = ShipmentRepository(session)
        self.alert_repository = RiskAlertRepository(session)
        self.commodity_repository = CommodityRepository(session)
        self.price_repository = MarketPriceRepository(session)

    async def summary(self) -> SummaryResponse:
        trades = await self.trade_repository.list()
        shipments = await self.shipment_repository.list()
        alerts = await self.alert_repository.list(resolved=False)
        margins = await self._trade_margins(trades)
        top_counterparties = self.counterparty_ranking(trades)[:5]
        return SummaryResponse(
            total_operations=len(trades),
            total_traded_volume=round(sum(trade.volume for trade in trades), 2),
            total_financial_exposure=round(sum(abs(calculate_trade_total(trade)) for trade in trades), 2),
            average_estimated_margin=round(sum(margins) / len(margins), 2) if margins else 0,
            open_operations=len([trade for trade in trades if trade.status not in {TradeStatus.SETTLED, TradeStatus.CANCELLED}]),
            delayed_shipments=len([shipment for shipment in shipments if calculate_delay_days(shipment) > 0]),
            critical_alerts=len([alert for alert in alerts if alert.severity == RiskSeverity.CRITICAL]),
            top_counterparties=top_counterparties,
        )

    async def exposure_by_region(self) -> list[dict]:
        totals: dict[str, float] = defaultdict(float)
        for trade in await self.trade_repository.list():
            totals[trade.region] += abs(calculate_trade_total(trade))
        return [{"region": region, "exposure": round(value, 2)} for region, value in sorted(totals.items())]

    async def volume_by_commodity(self) -> list[dict]:
        commodities = {commodity.id: commodity.name for commodity in await self.commodity_repository.list()}
        totals: dict[str, float] = defaultdict(float)
        for trade in await self.trade_repository.list():
            totals[commodities.get(trade.commodity_id, f"Commodity {trade.commodity_id}")] += trade.volume
        return [{"commodity": commodity, "volume": round(value, 2)} for commodity, value in sorted(totals.items())]

    async def trades_by_status(self) -> list[dict]:
        counter = Counter(trade.status.value for trade in await self.trade_repository.list())
        return [{"status": status.value, "count": counter.get(status.value, 0)} for status in TradeStatus]

    async def margin_analysis(self) -> list[MarginAnalysisItem]:
        commodities = {commodity.id: commodity.name for commodity in await self.commodity_repository.list()}
        grouped: dict[int, list[float]] = defaultdict(list)
        for trade in await self.trade_repository.list():
            price = await self.price_repository.latest_for_commodity(trade.commodity_id, trade.trade_date)
            margin = calculate_estimated_margin(trade, price)
            if margin is not None:
                grouped[trade.commodity_id].append(margin)
        return [
            MarginAnalysisItem(
                commodity_id=commodity_id,
                commodity=commodities.get(commodity_id, f"Commodity {commodity_id}"),
                average_margin=round(sum(values) / len(values), 2),
                negative_trades=len([value for value in values if value < 0]),
            )
            for commodity_id, values in grouped.items()
        ]

    async def volatility(self, days: int = 30) -> list[VolatilityItem]:
        start_date = date.today() - timedelta(days=days)
        items: list[VolatilityItem] = []
        for commodity in await self.commodity_repository.list(active_only=True):
            prices = await self.price_repository.list_between(commodity.id, start_date, date.today())
            items.append(
                VolatilityItem(
                    commodity_id=commodity.id,
                    commodity=commodity.name,
                    volatility_percent=calculate_simple_volatility(prices),
                )
            )
        return sorted(items, key=lambda item: item.volatility_percent, reverse=True)

    async def delayed_shipments(self) -> list[dict]:
        delayed = []
        for shipment in await self.shipment_repository.list():
            delay_days = calculate_delay_days(shipment)
            if delay_days > 0 and shipment.status != ShipmentStatus.CANCELLED:
                delayed.append(
                    {
                        "shipment_id": shipment.id,
                        "trade_operation_id": shipment.trade_operation_id,
                        "origin": shipment.origin,
                        "destination": shipment.destination,
                        "status": shipment.status.value,
                        "delay_days": delay_days,
                    }
                )
        return sorted(delayed, key=lambda item: item["delay_days"], reverse=True)

    async def negative_margin_trades(self) -> list[dict]:
        trades = []
        for trade in await self.trade_repository.list():
            price = await self.price_repository.latest_for_commodity(trade.commodity_id, trade.trade_date)
            margin = calculate_estimated_margin(trade, price)
            if margin is not None and margin < 0:
                trades.append({"trade_id": trade.id, "trade_code": trade.trade_code, "estimated_margin": margin})
        return sorted(trades, key=lambda item: item["estimated_margin"])

    @staticmethod
    def counterparty_ranking(trades) -> list[dict]:
        totals: dict[str, float] = defaultdict(float)
        for trade in trades:
            totals[trade.counterparty] += trade.volume
        return [
            {"counterparty": counterparty, "volume": round(volume, 2)}
            for counterparty, volume in sorted(totals.items(), key=lambda item: item[1], reverse=True)
        ]

    async def _trade_margins(self, trades) -> list[float]:
        margins = []
        for trade in trades:
            price = await self.price_repository.latest_for_commodity(trade.commodity_id, trade.trade_date)
            margin = calculate_estimated_margin(trade, price)
            if margin is not None:
                margins.append(margin)
        return margins

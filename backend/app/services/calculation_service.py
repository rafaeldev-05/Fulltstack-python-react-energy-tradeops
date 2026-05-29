from datetime import date
from statistics import pstdev

from app.models.enums import OperationType, ShipmentStatus
from app.models.logistics_shipment import LogisticsShipment
from app.models.market_price import MarketPrice
from app.models.trade_operation import TradeOperation


def calculate_price_variation(previous_price: float | None, current_price: float) -> float:
    if not previous_price:
        return 0
    return round(((current_price - previous_price) / previous_price) * 100, 4)


def calculate_trade_total(trade: TradeOperation) -> float:
    return round(trade.volume * trade.unit_price, 2)


def calculate_trade_exposure(trade: TradeOperation) -> float:
    direction = 1 if trade.operation_type == OperationType.BUY else -1
    return round(direction * calculate_trade_total(trade), 2)


def calculate_estimated_margin(trade: TradeOperation, market_price: MarketPrice | None) -> float | None:
    if not market_price:
        return None
    if trade.operation_type == OperationType.BUY:
        margin_per_unit = market_price.price - trade.unit_price
    else:
        margin_per_unit = trade.unit_price - market_price.price
    return round(margin_per_unit * trade.volume, 2)


def calculate_simple_volatility(prices: list[MarketPrice]) -> float:
    variations = [price.variation_percent for price in prices if price.variation_percent is not None]
    if len(variations) < 2:
        return 0
    return round(pstdev(variations), 4)


def calculate_delay_days(shipment: LogisticsShipment, today: date | None = None) -> int:
    today = today or date.today()
    if shipment.status == ShipmentStatus.CANCELLED:
        return 0
    if shipment.actual_arrival:
        return max((shipment.actual_arrival - shipment.estimated_arrival).days, 0)
    if shipment.status in {ShipmentStatus.DELIVERED, ShipmentStatus.CANCELLED}:
        return 0
    return max((today - shipment.estimated_arrival).days, 0)


def group_sum(items: list[dict], key: str, value: str) -> list[dict]:
    totals: dict[str, float] = {}
    for item in items:
        totals[item[key]] = totals.get(item[key], 0) + float(item[value])
    return [{"name": name, "value": round(total, 2)} for name, total in sorted(totals.items())]

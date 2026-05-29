from datetime import date, timedelta

from app.models.enums import OperationType, ShipmentStatus, TransportMode
from app.models.logistics_shipment import LogisticsShipment
from app.models.market_price import MarketPrice
from app.models.trade_operation import TradeOperation
from app.services.calculation_service import (
    calculate_delay_days,
    calculate_estimated_margin,
    calculate_price_variation,
    calculate_trade_exposure,
)


def test_price_variation():
    assert calculate_price_variation(100, 110) == 10
    assert calculate_price_variation(None, 110) == 0


def test_buy_margin_and_exposure():
    trade = TradeOperation(
        trade_code="TEST-001",
        operation_type=OperationType.BUY,
        commodity_id=1,
        volume=1_000,
        unit_price=80,
        region="Europe",
        counterparty="Test",
        trade_date=date.today(),
        settlement_date=date.today(),
    )
    price = MarketPrice(commodity_id=1, reference_date=date.today(), price=85)
    assert calculate_trade_exposure(trade) == 80_000
    assert calculate_estimated_margin(trade, price) == 5_000


def test_shipment_delay_days():
    shipment = LogisticsShipment(
        trade_operation_id=1,
        origin="Houston",
        destination="Rotterdam",
        transport_mode=TransportMode.SHIP,
        estimated_departure=date.today() - timedelta(days=10),
        estimated_arrival=date.today() - timedelta(days=2),
        status=ShipmentStatus.IN_TRANSIT,
    )
    assert calculate_delay_days(shipment) == 2

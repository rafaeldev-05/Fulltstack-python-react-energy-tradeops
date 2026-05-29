from datetime import date, timedelta
from random import Random

from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select

from app.models.commodity import Commodity
from app.models.enums import OperationType, RiskSeverity, ShipmentStatus, TradeStatus, TransportMode
from app.models.logistics_shipment import LogisticsShipment
from app.models.market_price import MarketPrice
from app.models.risk_alert import RiskAlert
from app.models.trade_operation import TradeOperation
from app.services.calculation_service import calculate_price_variation


async def seed_database(session: AsyncSession) -> None:
    existing = await session.execute(select(Commodity).limit(1))
    if existing.scalar_one_or_none():
        return

    random = Random(42)
    today = date.today()
    commodities = [
        Commodity(name="Brent Crude Oil", symbol="BRENT", category="Crude Oil", unit="barrel"),
        Commodity(name="WTI Crude Oil", symbol="WTI", category="Crude Oil", unit="barrel"),
        Commodity(name="Natural Gas", symbol="NG", category="Gas", unit="MMBtu"),
        Commodity(name="Diesel", symbol="DSL", category="Refined Products", unit="barrel"),
        Commodity(name="Gasoline", symbol="RBOB", category="Refined Products", unit="barrel"),
        Commodity(name="Naphtha", symbol="NAPH", category="Petrochemicals", unit="metric ton"),
        Commodity(name="Polypropylene", symbol="PP", category="Polymers", unit="metric ton"),
        Commodity(name="Polyethylene", symbol="PE", category="Polymers", unit="metric ton"),
    ]
    session.add_all(commodities)
    await session.commit()
    for commodity in commodities:
        await session.refresh(commodity)

    base_prices = {
        "BRENT": 86.5,
        "WTI": 81.2,
        "NG": 3.4,
        "DSL": 108.0,
        "RBOB": 99.5,
        "NAPH": 705.0,
        "PP": 1_135.0,
        "PE": 1_080.0,
    }
    price_by_day: dict[tuple[int, date], float] = {}
    for commodity in commodities:
        price = base_prices[commodity.symbol]
        previous_price: float | None = None
        for offset in range(89, -1, -1):
            reference_date = today - timedelta(days=offset)
            daily_noise = random.gauss(0, 0.018)
            if commodity.category in {"Polymers", "Petrochemicals"}:
                daily_noise += random.gauss(0, 0.01)
            price = max(price * (1 + daily_noise), 0.5)
            variation = calculate_price_variation(previous_price, price)
            session.add(
                MarketPrice(
                    commodity_id=commodity.id,
                    reference_date=reference_date,
                    price=round(price, 2),
                    currency="USD",
                    source="SIMULATED_MARKET_FEED",
                    variation_percent=variation,
                )
            )
            price_by_day[(commodity.id, reference_date)] = round(price, 2)
            previous_price = price
    await session.commit()

    regions = ["North America", "South America", "Europe", "Asia Pacific", "Middle East"]
    counterparties = [
        "Aurora Energy Trading",
        "BlueHarbor Commodities",
        "Caspian Petrochem",
        "Delta Refining Group",
        "Equinox Supply Co.",
        "Meridian Fuels",
        "Northstar Gas & Power",
        "Orion PetroTrade",
        "Pacific Terminal Partners",
        "Zenith Polymer Markets",
    ]
    statuses = [
        TradeStatus.DRAFT,
        TradeStatus.CONFIRMED,
        TradeStatus.IN_TRANSIT,
        TradeStatus.SETTLED,
        TradeStatus.CANCELLED,
    ]
    trades: list[TradeOperation] = []
    for index in range(1, 101):
        commodity = random.choice(commodities)
        trade_date = today - timedelta(days=random.randint(1, 80))
        market_price = price_by_day[(commodity.id, trade_date)]
        operation_type = random.choice([OperationType.BUY, OperationType.SELL])
        # A wider spread creates realistic positive and negative margin scenarios.
        negotiated_price = round(market_price * (1 + random.uniform(-0.09, 0.09)), 2)
        volume_multiplier = 1_000 if commodity.unit in {"barrel", "metric ton"} else 25_000
        trade = TradeOperation(
            trade_code=f"ETP-{today.year}-{index:04d}",
            operation_type=operation_type,
            commodity_id=commodity.id,
            volume=round(random.uniform(5, 90) * volume_multiplier, 2),
            unit_price=max(negotiated_price, 0.5),
            currency="USD",
            region=random.choice(regions),
            counterparty=random.choice(counterparties),
            trade_date=trade_date,
            settlement_date=trade_date + timedelta(days=random.randint(7, 45)),
            status=random.choices(statuses, weights=[8, 28, 22, 35, 7])[0],
        )
        trades.append(trade)
    session.add_all(trades)
    await session.commit()
    for trade in trades:
        await session.refresh(trade)

    origin_ports = ["Houston", "Rotterdam", "Singapore", "Santos", "Ras Tanura", "Antwerp", "Busan", "Corpus Christi"]
    destination_ports = ["Newark", "Hamburg", "Shanghai", "Buenos Aires", "Fujairah", "Valencia", "Long Beach", "Callao"]
    shippable_trades = [trade for trade in trades if trade.status != TradeStatus.CANCELLED]
    for index, trade in enumerate(random.sample(shippable_trades, 60), start=1):
        departure = trade.trade_date + timedelta(days=random.randint(1, 8))
        arrival = departure + timedelta(days=random.randint(4, 24))
        status = random.choices(
            [ShipmentStatus.PLANNED, ShipmentStatus.IN_TRANSIT, ShipmentStatus.DELAYED, ShipmentStatus.DELIVERED, ShipmentStatus.CANCELLED],
            weights=[15, 32, 18, 30, 5],
        )[0]
        actual_arrival = None
        if status == ShipmentStatus.DELIVERED:
            actual_arrival = arrival + timedelta(days=random.choice([0, 0, 1, 2, 4]))
        if status == ShipmentStatus.DELAYED and arrival >= today:
            arrival = today - timedelta(days=random.randint(1, 9))
        session.add(
            LogisticsShipment(
                trade_operation_id=trade.id,
                origin=random.choice(origin_ports),
                destination=random.choice(destination_ports),
                transport_mode=random.choice(list(TransportMode)),
                estimated_departure=departure,
                estimated_arrival=arrival,
                actual_arrival=actual_arrival,
                status=status,
            )
        )
    await session.commit()

    seeded_alerts = [
        RiskAlert(
            title=f"Seeded risk review {index:02d}",
            description="Preloaded operational risk alert for portfolio demonstration and dashboard density.",
            severity=random.choices(
                [RiskSeverity.LOW, RiskSeverity.MEDIUM, RiskSeverity.HIGH, RiskSeverity.CRITICAL],
                weights=[25, 35, 25, 15],
            )[0],
            related_trade_id=random.choice(trades).id,
            resolved=random.choice([False, False, False, True]),
        )
        for index in range(1, 21)
    ]
    session.add_all(seeded_alerts)
    await session.commit()

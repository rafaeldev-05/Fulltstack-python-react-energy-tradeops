# Business Rules

## Market Prices

- Each price records the commodity, date, price, currency, source, and percentage change.
- Daily percentage change compares the current price with the previous price for the same commodity.
- Price history can be filtered by commodity and date range.

## Trade Operations

- Trade types are `BUY` and `SELL`.
- Trade statuses are `DRAFT`, `CONFIRMED`, `IN_TRANSIT`, `SETTLED`, and `CANCELLED`.
- Total value is `volume * unit_price`.
- Buys create positive exposure and sells create negative exposure.
- Estimated margin is `(market_price - unit_price) * volume` for buys and `(unit_price - market_price) * volume` for sells.
- Cancelled trades cannot be settled, and settled trades cannot be cancelled.
- The economic terms of a settled trade cannot be changed.

## Logistics

- Transport modes are `SHIP`, `PIPELINE`, `TRUCK`, and `RAIL`.
- Shipment statuses are `PLANNED`, `IN_TRANSIT`, `DELAYED`, `DELIVERED`, and `CANCELLED`.
- Delay calculations compare the estimated arrival with the actual arrival or the current date.
- Delayed shipments are highlighted and included in risk analytics.

## Risk Alerts

- Severity levels are `LOW`, `MEDIUM`, `HIGH`, and `CRITICAL`.
- Alerts cover margins below the configured threshold, delayed shipments, and high recent price volatility.
- Resolved alerts remain in the history.

## Analytics

The platform reports total trades, traded volume by commodity, total exposure and exposure by region, average estimated margin, trades by status, high-volatility commodities, negative-margin trades, delayed shipments, critical alerts, and the five largest counterparties by traded volume.

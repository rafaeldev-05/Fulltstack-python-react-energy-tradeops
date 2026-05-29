# Endpoints

Base URL local: `http://localhost:8000/api/v1`

## Commodities

- `POST /commodities`
- `GET /commodities`
- `GET /commodities/{commodity_id}`
- `PATCH /commodities/{commodity_id}`

## Market Prices

- `POST /market-prices`
- `GET /market-prices`
- `GET /market-prices/{commodity_id}`

## Trade Operations

- `POST /trades`
- `GET /trades`
- `GET /trades/{trade_id}`
- `PATCH /trades/{trade_id}`
- `PATCH /trades/{trade_id}/confirm`
- `PATCH /trades/{trade_id}/settle`
- `PATCH /trades/{trade_id}/cancel`

## Logistics

- `POST /shipments`
- `GET /shipments`
- `GET /shipments/{shipment_id}`
- `PATCH /shipments/{shipment_id}`
- `PATCH /shipments/{shipment_id}/mark-delivered`
- `PATCH /shipments/{shipment_id}/mark-delayed`

## Risk Alerts

- `GET /risk-alerts`
- `PATCH /risk-alerts/{alert_id}/resolve`
- `POST /risk-alerts/run-monitoring-cycle`

## Analytics

- `GET /analytics/summary`
- `GET /analytics/exposure-by-region`
- `GET /analytics/volume-by-commodity`
- `GET /analytics/trades-by-status`
- `GET /analytics/margin-analysis`
- `GET /analytics/volatility`
- `GET /analytics/delayed-shipments`

## System

- `GET /health`

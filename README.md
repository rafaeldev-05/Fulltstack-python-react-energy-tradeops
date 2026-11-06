# Energy TradeOps Platform

A full-stack portfolio project that simulates energy commodity trading, shipment tracking, and operational risk monitoring with synthetic data.

The platform tracks buy and sell trades, market prices, financial exposure, estimated margins, shipments, volatility, and risk alerts for commodities such as crude oil, natural gas, diesel, gasoline, naphtha, and petrochemicals.

## Technology stack

- **Backend:** Python, FastAPI, SQLModel, Pydantic, async SQLite, and an `asyncio` risk monitor.
- **Frontend:** React, TypeScript, Vite, Tailwind CSS, Axios, Recharts, and Lucide.

## Run the demo with Docker

With Docker and Docker Compose running, start the demo from the repository root:

```sh
docker compose up --build -d
```

Open [localhost:8088](http://localhost:8088). The demo uses synthetic data and stores changes in a Docker volume. Use `docker compose down` to stop the demo and keep the data.

## Run locally without Docker

Run the backend and frontend in separate terminals. See the [backend setup](backend/README.md) for Python and database configuration and the [frontend setup](frontend/README.md) for the Vite app.

- Web app: http://localhost:5173
- Interactive API docs: http://localhost:8000/docs

## Features

- **Executive Dashboard:** Review exposure, traded volume, estimated margins, critical alerts, and shipment delays.
- **Trade Operations:** List and filter trades, create orders, and confirm, settle, or cancel trades.
- **Market Prices:** Record prices and review price history and changes over time.
- **Logistics:** Create shipments and mark them as delayed or delivered.
- **Risk Center:** Review alerts by severity and resolve them.

With seeding enabled, a fresh database starts with eight commodities, 90 days of price history, 100 trades, 60 shipments, 20 initial alerts, and synthetic counterparties and regions. The risk monitor can generate additional alerts after seeding.

## Documentation

- [Architecture](docs/architecture.md)
- [REST endpoints](docs/endpoints.md)
- [Business rules](docs/business-rules.md)

## Planned work

- Authentication and role-based access for Trading, Risk, Finance, and Logistics.
- PostgreSQL migrations with Alembic.
- Live updates via WebSockets.
- Price curve imports from CSV files or external APIs.
- Integration tests for critical endpoints.
- Docker Compose for local setup.

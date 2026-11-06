# Architecture

Energy TradeOps Platform consists of a FastAPI backend and a React frontend.

## Backend

- `models` defines entities persisted with SQLModel.
- `schemas` defines Pydantic request and response contracts.
- `repositories` provides asynchronous data access.
- `services` applies business rules, calculates analytics, and validates workflow transitions.
- `api/routes` exposes HTTP endpoints.
- `workers` runs asynchronous risk monitoring.
- `utils/seed.py` populates a fresh database with synthetic data.

SQLite with `aiosqlite` is the default. The `DATABASE_URL` setting supports a PostgreSQL connection URL when an async PostgreSQL driver is installed.

## Frontend

- `components` contains shared layout, cards, badges, panels, and loading and error states.
- `pages` contains the operational screens.
- `services` contains the typed Axios client.
- `hooks` provides reusable asynchronous data loading.
- `types` defines TypeScript domain types.
- `utils` formats currencies, numbers, and percentages.

## Data flow

1. Users interact with React dashboards, tables, and forms.
2. The frontend sends REST requests under `/api/v1`.
3. FastAPI validates payloads with Pydantic and delegates to services.
4. Services apply business rules and persist data through repositories.
5. Analytics aggregate trade, price, shipment, and alert data.
6. The risk worker checks for risk conditions periodically and creates alerts.

# Energy TradeOps Backend

Asynchronous FastAPI service for trade operations, market prices, logistics, analytics, and risk alerts.

## Run locally

From the repository root, enter the backend directory and create a virtual environment with Python 3.10 or later.

```sh
cd backend
python -m venv .venv
```

Activate it with `source .venv/bin/activate` on macOS or Linux, or `.venv\Scripts\Activate.ps1` in Windows PowerShell. Then run:

```sh
python -m pip install -r requirements.txt
python -m uvicorn app.main:app --reload
```

Open the interactive API documentation at http://localhost:8000/docs. Run the backend tests from this directory with `python -m pytest`.

## Database and startup

The default database is SQLite in `energy_tradeops.db`. The `DATABASE_URL` setting can point to PostgreSQL if an asynchronous PostgreSQL driver is installed.

On startup, the app creates tables and can seed synthetic data and run a risk monitoring cycle. The periodic worker is in `app/workers/risk_monitor.py`.

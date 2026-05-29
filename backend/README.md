# Backend - Energy TradeOps Platform

API FastAPI assíncrona para operações de trading, preços de mercado, logística, analytics e alertas de risco.

## Rodar localmente

```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

No Linux/macOS, use `source venv/bin/activate`.

Swagger: http://localhost:8000/docs

## Banco

O padrão é SQLite em `energy_tradeops.db`. Para PostgreSQL futuramente, configure `DATABASE_URL` no `.env` usando um driver async compatível.

## Seed e worker

Ao iniciar, a API cria tabelas, popula dados simulados e executa um ciclo de monitoramento de risco. O worker assíncrono periódico fica em `app/workers/risk_monitor.py`.

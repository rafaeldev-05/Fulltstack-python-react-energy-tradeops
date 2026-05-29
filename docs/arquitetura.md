# Arquitetura

O Energy TradeOps Platform é dividido em backend FastAPI e frontend React.

## Backend

Camadas principais:

- `models`: entidades persistidas com SQLModel.
- `schemas`: contratos Pydantic de entrada e saída.
- `repositories`: acesso assíncrono aos dados.
- `services`: regras de negócio, cálculos, analytics e validações de workflow.
- `api/routes`: endpoints HTTP.
- `workers`: monitoramento assíncrono de risco.
- `utils/seed.py`: massa inicial de dados simulados.

O banco padrão é SQLite com `aiosqlite`, mas a configuração `DATABASE_URL` permite migrar para PostgreSQL com driver async.

## Frontend

Camadas principais:

- `components`: layout, cards, badges, painéis e estados de loading/erro.
- `pages`: telas operacionais.
- `services`: cliente Axios tipado.
- `hooks`: carregamento assíncrono reutilizável.
- `types`: tipos de domínio em TypeScript.
- `utils`: formatação de moeda, número e percentual.

## Fluxo de dados

1. Usuário interage com dashboards, tabelas ou formulários no React.
2. O frontend chama endpoints REST em `/api/v1`.
3. Rotas FastAPI validam payloads com Pydantic e delegam para services.
4. Services aplicam regras de negócio e usam repositories para persistência.
5. Analytics agregam dados de trades, preços, shipments e alertas.
6. Worker de risco executa verificações periódicas e cria alertas.

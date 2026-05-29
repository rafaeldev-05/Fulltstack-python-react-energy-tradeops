# Energy TradeOps Platform

Plataforma fullstack de portfólio para simular operações globais de trading de commodities energéticas, supply chain analytics e risk control.

## Objetivo

O projeto demonstra uma solução corporativa para acompanhar contratos de compra e venda, preços de mercado, exposição financeira, margem estimada, logística, volatilidade e alertas operacionais em commodities como petróleo, gás natural, diesel, gasolina, nafta e petroquímicos.

## Tecnologias

Backend:

- Python
- FastAPI
- SQLModel
- Pydantic
- SQLite com engine async
- Arquitetura preparada para PostgreSQL
- Worker assíncrono com `asyncio`

Frontend:

- React
- TypeScript
- Vite
- Tailwind CSS
- Axios
- Recharts
- lucide-react

## Arquitetura

```txt
backend/app
  models          Entidades SQLModel
  schemas         Contratos Pydantic
  repositories    Acesso a dados
  services        Regras de negócio e analytics
  api/routes      Endpoints REST
  workers         Monitoramento assíncrono de risco
  utils           Seed de dados

frontend/src
  components      UI reutilizável
  pages           Telas operacionais
  services        Cliente HTTP
  hooks           Hooks de carregamento
  types           Tipos TypeScript
  utils           Formatadores
```

## Rodar Backend

```bash
cd backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Swagger/OpenAPI: http://localhost:8000/docs

## Rodar Frontend

```bash
cd frontend
npm install
npm run dev
```

Aplicação: http://localhost:5173

## Seed de Dados

Na primeira execução, a API cria:

- 8 commodities;
- 90 dias de histórico de preços;
- 100 operações de trading;
- 60 shipments;
- 20 alertas iniciais de risco;
- regiões e contrapartes fictícias.

## Principais Endpoints

- `GET /api/v1/analytics/summary`
- `GET /api/v1/trades`
- `POST /api/v1/trades`
- `PATCH /api/v1/trades/{id}/confirm`
- `PATCH /api/v1/trades/{id}/settle`
- `PATCH /api/v1/trades/{id}/cancel`
- `GET /api/v1/market-prices/{commodity_id}`
- `POST /api/v1/shipments`
- `GET /api/v1/risk-alerts`

Lista completa em `docs/endpoints.md`.

## Telas

- Dashboard executivo com exposição, volume, margem, alertas críticos, atrasos e gráficos.
- Trade Operations com listagem, filtros, criação, confirmação, liquidação e cancelamento.
- Market Prices com cadastro de preço, histórico e evolução.
- Logistics com criação de shipment, marcação de atraso e entrega.
- Risk Center com alertas por severidade e resolução.

## Regras de Negócio

- Margem estimada compara preço negociado com preço de mercado.
- Compra gera exposição positiva; venda gera exposição negativa.
- Trades canceladas não podem ser liquidadas.
- Trades liquidadas não podem ser canceladas.
- Shipments atrasados geram alertas.
- Alta volatilidade gera alerta automático.
- Margem negativa acima do limite configurado gera alerta de risco.

Mais detalhes em `docs/regras-de-negocio.md`.

## Próximos Passos

- Autenticação e RBAC por área: Trading, Risk, Finance e Logistics.
- PostgreSQL com migrações Alembic.
- WebSockets para atualização em tempo real.
- Importação de curvas de preço via CSV/API externa.
- Testes de integração para endpoints críticos.
- Docker Compose para ambiente completo.

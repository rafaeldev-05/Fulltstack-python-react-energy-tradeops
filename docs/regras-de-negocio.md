# Regras de Negócio

## Market Prices

- Cada preço registra commodity, data, preço, moeda, fonte e variação percentual.
- A variação diária é calculada comparando o preço atual com o preço anterior da mesma commodity.
- O histórico pode ser consultado por commodity e período.

## Trade Operations

- Tipos aceitos: `BUY` e `SELL`.
- Status aceitos: `DRAFT`, `CONFIRMED`, `IN_TRANSIT`, `SETTLED`, `CANCELLED`.
- Valor total: `volume * unit_price`.
- Exposição: positiva para compra e negativa para venda.
- Margem estimada:
  - Compra: `(market_price - unit_price) * volume`.
  - Venda: `(unit_price - market_price) * volume`.
- Operação cancelada não pode ser liquidada.
- Operação liquidada não pode ser cancelada.
- Termos econômicos de operação liquidada não devem ser alterados.

## Logistics

- Modais aceitos: `SHIP`, `PIPELINE`, `TRUCK`, `RAIL`.
- Status aceitos: `PLANNED`, `IN_TRANSIT`, `DELAYED`, `DELIVERED`, `CANCELLED`.
- Atraso é calculado comparando chegada estimada com chegada real ou data atual.
- Shipments atrasados são destacados e alimentam analytics de risco.

## Risk Alerts

- Severidades aceitas: `LOW`, `MEDIUM`, `HIGH`, `CRITICAL`.
- Alertas são criados para:
  - margem negativa acima do limite configurado;
  - shipment atrasado;
  - volatilidade elevada nos últimos dias.
- Alertas podem ser resolvidos, mas permanecem no histórico.

## Analytics

Indicadores implementados:

- total de operações;
- volume negociado por commodity;
- exposição financeira total;
- exposição por região;
- margem média estimada;
- operações por status;
- commodities com maior volatilidade;
- operações com margem negativa;
- shipments atrasados;
- quantidade de alertas críticos;
- top 5 contrapartes por volume negociado.

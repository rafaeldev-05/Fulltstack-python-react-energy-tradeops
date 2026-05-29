import axios from "axios";

import {
  Commodity,
  LogisticsShipment,
  MarketPrice,
  RiskAlert,
  RiskSeverity,
  ShipmentStatus,
  Summary,
  TradeOperation,
  TradeStatus,
} from "../types/domain";

export const api = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL ?? "http://localhost:8000/api/v1",
});

export const endpoints = {
  commodities: {
    list: () => api.get<Commodity[]>("/commodities").then((response) => response.data),
  },
  analytics: {
    summary: () => api.get<Summary>("/analytics/summary").then((response) => response.data),
    exposureByRegion: () => api.get<Array<{ region: string; exposure: number }>>("/analytics/exposure-by-region").then((response) => response.data),
    volumeByCommodity: () => api.get<Array<{ commodity: string; volume: number }>>("/analytics/volume-by-commodity").then((response) => response.data),
    tradesByStatus: () => api.get<Array<{ status: TradeStatus; count: number }>>("/analytics/trades-by-status").then((response) => response.data),
    marginAnalysis: () => api.get<Array<{ commodity: string; average_margin: number; negative_trades: number }>>("/analytics/margin-analysis").then((response) => response.data),
    volatility: () => api.get<Array<{ commodity: string; volatility_percent: number }>>("/analytics/volatility").then((response) => response.data),
    delayedShipments: () => api.get<Array<{ shipment_id: number; trade_operation_id: number; delay_days: number }>>("/analytics/delayed-shipments").then((response) => response.data),
  },
  trades: {
    list: (params?: Record<string, string>) => api.get<TradeOperation[]>("/trades", { params }).then((response) => response.data),
    create: (payload: Partial<TradeOperation>) => api.post<TradeOperation>("/trades", payload).then((response) => response.data),
    confirm: (id: number) => api.patch<TradeOperation>(`/trades/${id}/confirm`).then((response) => response.data),
    settle: (id: number) => api.patch<TradeOperation>(`/trades/${id}/settle`).then((response) => response.data),
    cancel: (id: number) => api.patch<TradeOperation>(`/trades/${id}/cancel`).then((response) => response.data),
  },
  prices: {
    list: (commodityId?: number) => api.get<MarketPrice[]>(commodityId ? `/market-prices/${commodityId}` : "/market-prices").then((response) => response.data),
    create: (payload: Partial<MarketPrice>) => api.post<MarketPrice>("/market-prices", payload).then((response) => response.data),
  },
  shipments: {
    list: (status?: ShipmentStatus) => api.get<LogisticsShipment[]>("/shipments", { params: { status } }).then((response) => response.data),
    create: (payload: Partial<LogisticsShipment>) => api.post<LogisticsShipment>("/shipments", payload).then((response) => response.data),
    markDelayed: (id: number) => api.patch<LogisticsShipment>(`/shipments/${id}/mark-delayed`).then((response) => response.data),
    markDelivered: (id: number) => api.patch<LogisticsShipment>(`/shipments/${id}/mark-delivered`).then((response) => response.data),
  },
  alerts: {
    list: (severity?: RiskSeverity) => api.get<RiskAlert[]>("/risk-alerts", { params: { severity, resolved: false } }).then((response) => response.data),
    resolve: (id: number) => api.patch<RiskAlert>(`/risk-alerts/${id}/resolve`).then((response) => response.data),
  },
};

export type OperationType = "BUY" | "SELL";
export type TradeStatus = "DRAFT" | "CONFIRMED" | "IN_TRANSIT" | "SETTLED" | "CANCELLED";
export type TransportMode = "SHIP" | "PIPELINE" | "TRUCK" | "RAIL";
export type ShipmentStatus = "PLANNED" | "IN_TRANSIT" | "DELAYED" | "DELIVERED" | "CANCELLED";
export type RiskSeverity = "LOW" | "MEDIUM" | "HIGH" | "CRITICAL";

export interface Commodity {
  id: number;
  name: string;
  symbol: string;
  category: string;
  unit: string;
  active: boolean;
}

export interface MarketPrice {
  id: number;
  commodity_id: number;
  reference_date: string;
  price: number;
  currency: string;
  source: string;
  variation_percent: number;
}

export interface TradeOperation {
  id: number;
  trade_code: string;
  operation_type: OperationType;
  commodity_id: number;
  volume: number;
  unit_price: number;
  currency: string;
  region: string;
  counterparty: string;
  trade_date: string;
  settlement_date: string;
  status: TradeStatus;
  created_at: string;
  total_value?: number;
  exposure?: number;
  estimated_margin?: number | null;
}

export interface LogisticsShipment {
  id: number;
  trade_operation_id: number;
  origin: string;
  destination: string;
  transport_mode: TransportMode;
  estimated_departure: string;
  estimated_arrival: string;
  actual_arrival?: string | null;
  status: ShipmentStatus;
  delay_days: number;
}

export interface RiskAlert {
  id: number;
  title: string;
  description: string;
  severity: RiskSeverity;
  related_trade_id?: number | null;
  created_at: string;
  resolved: boolean;
}

export interface Summary {
  total_operations: number;
  total_traded_volume: number;
  total_financial_exposure: number;
  average_estimated_margin: number;
  open_operations: number;
  delayed_shipments: number;
  critical_alerts: number;
  top_counterparties: Array<{ counterparty: string; volume: number }>;
}

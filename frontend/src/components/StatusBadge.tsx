import { RiskSeverity, ShipmentStatus, TradeStatus } from "../types/domain";

type Status = TradeStatus | ShipmentStatus | RiskSeverity | "BUY" | "SELL";

const colors: Record<string, string> = {
  DRAFT: "bg-slate-100 text-slate-700",
  CONFIRMED: "bg-blue-100 text-blue-700",
  IN_TRANSIT: "bg-cyan-100 text-cyan-700",
  SETTLED: "bg-emerald-100 text-emerald-700",
  CANCELLED: "bg-slate-200 text-slate-600",
  PLANNED: "bg-indigo-100 text-indigo-700",
  DELAYED: "bg-amber-100 text-amber-800",
  DELIVERED: "bg-emerald-100 text-emerald-700",
  LOW: "bg-slate-100 text-slate-700",
  MEDIUM: "bg-amber-100 text-amber-800",
  HIGH: "bg-orange-100 text-orange-800",
  CRITICAL: "bg-red-100 text-red-700",
  BUY: "bg-emerald-100 text-emerald-700",
  SELL: "bg-blue-100 text-blue-700",
};

export function StatusBadge({ status }: { status: Status }) {
  return (
    <span className={`inline-flex min-w-20 items-center justify-center rounded-md px-2.5 py-1 text-xs font-semibold ${colors[status]}`}>
      {status.replace("_", " ")}
    </span>
  );
}

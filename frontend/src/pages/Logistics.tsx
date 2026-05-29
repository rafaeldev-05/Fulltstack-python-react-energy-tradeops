import { FormEvent, useState } from "react";
import { CheckCircle2, Plus, TimerOff } from "lucide-react";

import { Panel } from "../components/Panel";
import { ErrorBlock, LoadingBlock } from "../components/StateBlock";
import { StatusBadge } from "../components/StatusBadge";
import { endpoints } from "../services/api";
import { LogisticsShipment, ShipmentStatus, TradeOperation, TransportMode } from "../types/domain";
import { useAsyncData } from "../hooks/useAsyncData";

const modes: TransportMode[] = ["SHIP", "PIPELINE", "TRUCK", "RAIL"];
const statuses: ShipmentStatus[] = ["PLANNED", "IN_TRANSIT", "DELAYED", "DELIVERED", "CANCELLED"];

const initialForm = {
  trade_operation_id: "",
  origin: "",
  destination: "",
  transport_mode: "SHIP" as TransportMode,
  estimated_departure: new Date().toISOString().slice(0, 10),
  estimated_arrival: new Date(Date.now() + 10 * 86400000).toISOString().slice(0, 10),
};

export function Logistics() {
  const [statusFilter, setStatusFilter] = useState("");
  const [form, setForm] = useState(initialForm);

  const { data, loading, error, refresh } = useAsyncData<{ shipments: LogisticsShipment[]; trades: TradeOperation[] }>(async () => {
    const [shipments, trades] = await Promise.all([
      endpoints.shipments.list(statusFilter ? (statusFilter as ShipmentStatus) : undefined),
      endpoints.trades.list(),
    ]);
    return { shipments, trades };
  }, [statusFilter]);

  async function submitShipment(event: FormEvent) {
    event.preventDefault();
    await endpoints.shipments.create({ ...form, trade_operation_id: Number(form.trade_operation_id) });
    setForm(initialForm);
    refresh();
  }

  async function action(id: number, kind: "delayed" | "delivered") {
    if (kind === "delayed") await endpoints.shipments.markDelayed(id);
    if (kind === "delivered") await endpoints.shipments.markDelivered(id);
    refresh();
  }

  if (loading) return <LoadingBlock />;
  if (error || !data) return <ErrorBlock message={error ?? "Logistics unavailable"} />;

  return (
    <div className="space-y-6">
      <Panel title="Create Shipment">
        <form className="grid gap-4 md:grid-cols-3 xl:grid-cols-6" onSubmit={submitShipment}>
          <select className="rounded-md border border-slate-300 px-3 py-2" required value={form.trade_operation_id} onChange={(event) => setForm({ ...form, trade_operation_id: event.target.value })}>
            <option value="">Trade</option>
            {data.trades.slice(0, 80).map((trade) => <option key={trade.id} value={trade.id}>{trade.trade_code}</option>)}
          </select>
          <input className="rounded-md border border-slate-300 px-3 py-2" placeholder="Origin" required value={form.origin} onChange={(event) => setForm({ ...form, origin: event.target.value })} />
          <input className="rounded-md border border-slate-300 px-3 py-2" placeholder="Destination" required value={form.destination} onChange={(event) => setForm({ ...form, destination: event.target.value })} />
          <select className="rounded-md border border-slate-300 px-3 py-2" value={form.transport_mode} onChange={(event) => setForm({ ...form, transport_mode: event.target.value as TransportMode })}>
            {modes.map((mode) => <option key={mode}>{mode}</option>)}
          </select>
          <input className="rounded-md border border-slate-300 px-3 py-2" type="date" value={form.estimated_departure} onChange={(event) => setForm({ ...form, estimated_departure: event.target.value })} />
          <input className="rounded-md border border-slate-300 px-3 py-2" type="date" value={form.estimated_arrival} onChange={(event) => setForm({ ...form, estimated_arrival: event.target.value })} />
          <button className="inline-flex items-center justify-center gap-2 rounded-md bg-pipeline px-4 py-2 font-semibold text-white hover:bg-offshore md:col-span-3 xl:col-span-1" type="submit">
            <Plus size={17} />
            Create
          </button>
        </form>
      </Panel>

      <Panel
        title="Shipment Control"
        action={
          <select className="rounded-md border border-slate-300 px-3 py-2 text-sm" value={statusFilter} onChange={(event) => setStatusFilter(event.target.value)}>
            <option value="">All statuses</option>
            {statuses.map((status) => <option key={status}>{status}</option>)}
          </select>
        }
      >
        <div className="table-scroll overflow-x-auto">
          <table className="w-full min-w-[980px] text-left text-sm">
            <thead className="bg-slate-50 text-xs uppercase text-slate-500">
              <tr>
                <th className="px-3 py-3">Trade</th>
                <th className="px-3 py-3">Route</th>
                <th className="px-3 py-3">Mode</th>
                <th className="px-3 py-3">Departure</th>
                <th className="px-3 py-3">Arrival ETA</th>
                <th className="px-3 py-3 text-right">Delay</th>
                <th className="px-3 py-3">Status</th>
                <th className="px-3 py-3">Actions</th>
              </tr>
            </thead>
            <tbody>
              {data.shipments.map((shipment) => (
                <tr key={shipment.id} className={`border-b border-slate-100 ${shipment.delay_days > 0 ? "bg-amber-50/60" : ""}`}>
                  <td className="px-3 py-3 font-semibold text-ink">{shipment.trade_operation_id}</td>
                  <td className="px-3 py-3">{shipment.origin} to {shipment.destination}</td>
                  <td className="px-3 py-3">{shipment.transport_mode}</td>
                  <td className="px-3 py-3">{shipment.estimated_departure}</td>
                  <td className="px-3 py-3">{shipment.estimated_arrival}</td>
                  <td className={`px-3 py-3 text-right font-semibold ${shipment.delay_days > 0 ? "text-amber-800" : "text-slate-500"}`}>{shipment.delay_days}d</td>
                  <td className="px-3 py-3"><StatusBadge status={shipment.status} /></td>
                  <td className="px-3 py-3">
                    <div className="flex gap-2">
                      <button title="Mark delayed" className="rounded-md border border-slate-300 p-2 text-amber-700 hover:bg-amber-50" onClick={() => action(shipment.id, "delayed")} type="button"><TimerOff size={16} /></button>
                      <button title="Mark delivered" className="rounded-md border border-slate-300 p-2 text-emerald-700 hover:bg-emerald-50" onClick={() => action(shipment.id, "delivered")} type="button"><CheckCircle2 size={16} /></button>
                    </div>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </Panel>
    </div>
  );
}

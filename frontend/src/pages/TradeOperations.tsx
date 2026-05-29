import { FormEvent, useState } from "react";
import { CheckCircle2, CircleX, Plus, ShieldCheck } from "lucide-react";

import { Panel } from "../components/Panel";
import { ErrorBlock, LoadingBlock } from "../components/StateBlock";
import { StatusBadge } from "../components/StatusBadge";
import { endpoints } from "../services/api";
import { Commodity, OperationType, TradeOperation, TradeStatus } from "../types/domain";
import { money, number } from "../utils/format";
import { useAsyncData } from "../hooks/useAsyncData";

const regions = ["North America", "South America", "Europe", "Asia Pacific", "Middle East"];
const statuses: TradeStatus[] = ["DRAFT", "CONFIRMED", "IN_TRANSIT", "SETTLED", "CANCELLED"];
const operationTypes: OperationType[] = ["BUY", "SELL"];

const initialForm = {
  trade_code: "",
  operation_type: "BUY" as OperationType,
  commodity_id: "",
  volume: "",
  unit_price: "",
  region: "North America",
  counterparty: "",
  trade_date: new Date().toISOString().slice(0, 10),
  settlement_date: new Date(Date.now() + 14 * 86400000).toISOString().slice(0, 10),
};

export function TradeOperations() {
  const [filters, setFilters] = useState({ commodity_id: "", region: "", status: "", operation_type: "" });
  const [form, setForm] = useState(initialForm);

  const { data, loading, error, refresh } = useAsyncData<{ trades: TradeOperation[]; commodities: Commodity[] }>(async () => {
    const params: Record<string, string> = Object.fromEntries(Object.entries(filters).filter(([, value]) => value));
    const [trades, commodities] = await Promise.all([endpoints.trades.list(params), endpoints.commodities.list()]);
    return { trades, commodities };
  }, [filters.commodity_id, filters.region, filters.status, filters.operation_type]);

  async function submitTrade(event: FormEvent) {
    event.preventDefault();
    await endpoints.trades.create({
      ...form,
      commodity_id: Number(form.commodity_id),
      volume: Number(form.volume),
      unit_price: Number(form.unit_price),
      currency: "USD",
    });
    setForm({ ...initialForm, trade_code: `ETP-MAN-${Date.now().toString().slice(-6)}` });
    refresh();
  }

  async function action(id: number, kind: "confirm" | "settle" | "cancel") {
    if (kind === "confirm") await endpoints.trades.confirm(id);
    if (kind === "settle") await endpoints.trades.settle(id);
    if (kind === "cancel") await endpoints.trades.cancel(id);
    refresh();
  }

  if (loading) return <LoadingBlock />;
  if (error || !data) return <ErrorBlock message={error ?? "Trade operations unavailable"} />;

  const commodityName = (id: number) => data.commodities.find((item) => item.id === id)?.symbol ?? id;

  return (
    <div className="space-y-6">
      <Panel title="Create Trade Operation">
        <form className="grid gap-4 md:grid-cols-2 xl:grid-cols-5" onSubmit={submitTrade}>
          <input className="rounded-md border border-slate-300 px-3 py-2" placeholder="Trade code" required value={form.trade_code} onChange={(event) => setForm({ ...form, trade_code: event.target.value })} />
          <select className="rounded-md border border-slate-300 px-3 py-2" value={form.operation_type} onChange={(event) => setForm({ ...form, operation_type: event.target.value as OperationType })}>
            {operationTypes.map((type) => <option key={type}>{type}</option>)}
          </select>
          <select className="rounded-md border border-slate-300 px-3 py-2" required value={form.commodity_id} onChange={(event) => setForm({ ...form, commodity_id: event.target.value })}>
            <option value="">Commodity</option>
            {data.commodities.map((commodity) => <option key={commodity.id} value={commodity.id}>{commodity.name}</option>)}
          </select>
          <input className="rounded-md border border-slate-300 px-3 py-2" placeholder="Volume" required type="number" value={form.volume} onChange={(event) => setForm({ ...form, volume: event.target.value })} />
          <input className="rounded-md border border-slate-300 px-3 py-2" placeholder="Unit price" required type="number" step="0.01" value={form.unit_price} onChange={(event) => setForm({ ...form, unit_price: event.target.value })} />
          <select className="rounded-md border border-slate-300 px-3 py-2" value={form.region} onChange={(event) => setForm({ ...form, region: event.target.value })}>
            {regions.map((region) => <option key={region}>{region}</option>)}
          </select>
          <input className="rounded-md border border-slate-300 px-3 py-2" placeholder="Counterparty" required value={form.counterparty} onChange={(event) => setForm({ ...form, counterparty: event.target.value })} />
          <input className="rounded-md border border-slate-300 px-3 py-2" required type="date" value={form.trade_date} onChange={(event) => setForm({ ...form, trade_date: event.target.value })} />
          <input className="rounded-md border border-slate-300 px-3 py-2" required type="date" value={form.settlement_date} onChange={(event) => setForm({ ...form, settlement_date: event.target.value })} />
          <button className="inline-flex items-center justify-center gap-2 rounded-md bg-pipeline px-4 py-2 font-semibold text-white hover:bg-offshore" type="submit">
            <Plus size={17} />
            Create
          </button>
        </form>
      </Panel>

      <Panel title="Operations Blotter">
        <div className="mb-4 grid gap-3 md:grid-cols-4">
          <select className="rounded-md border border-slate-300 px-3 py-2" value={filters.commodity_id} onChange={(event) => setFilters({ ...filters, commodity_id: event.target.value })}>
            <option value="">All commodities</option>
            {data.commodities.map((commodity) => <option key={commodity.id} value={commodity.id}>{commodity.symbol}</option>)}
          </select>
          <select className="rounded-md border border-slate-300 px-3 py-2" value={filters.region} onChange={(event) => setFilters({ ...filters, region: event.target.value })}>
            <option value="">All regions</option>
            {regions.map((region) => <option key={region}>{region}</option>)}
          </select>
          <select className="rounded-md border border-slate-300 px-3 py-2" value={filters.status} onChange={(event) => setFilters({ ...filters, status: event.target.value })}>
            <option value="">All statuses</option>
            {statuses.map((status) => <option key={status}>{status}</option>)}
          </select>
          <select className="rounded-md border border-slate-300 px-3 py-2" value={filters.operation_type} onChange={(event) => setFilters({ ...filters, operation_type: event.target.value })}>
            <option value="">Buy and sell</option>
            {operationTypes.map((type) => <option key={type}>{type}</option>)}
          </select>
        </div>

        <div className="table-scroll overflow-x-auto">
          <table className="min-w-[1100px] w-full text-left text-sm">
            <thead className="bg-slate-50 text-xs uppercase text-slate-500">
              <tr>
                <th className="px-3 py-3">Code</th>
                <th className="px-3 py-3">Type</th>
                <th className="px-3 py-3">Commodity</th>
                <th className="px-3 py-3">Region</th>
                <th className="px-3 py-3">Counterparty</th>
                <th className="px-3 py-3 text-right">Volume</th>
                <th className="px-3 py-3 text-right">Exposure</th>
                <th className="px-3 py-3 text-right">Margin</th>
                <th className="px-3 py-3">Status</th>
                <th className="px-3 py-3">Actions</th>
              </tr>
            </thead>
            <tbody>
              {data.trades.map((trade) => (
                <tr key={trade.id} className="border-b border-slate-100 hover:bg-slate-50">
                  <td className="px-3 py-3 font-semibold text-ink">{trade.trade_code}</td>
                  <td className="px-3 py-3"><StatusBadge status={trade.operation_type} /></td>
                  <td className="px-3 py-3">{commodityName(trade.commodity_id)}</td>
                  <td className="px-3 py-3">{trade.region}</td>
                  <td className="px-3 py-3">{trade.counterparty}</td>
                  <td className="px-3 py-3 text-right">{number(trade.volume)}</td>
                  <td className="px-3 py-3 text-right">{money(trade.exposure)}</td>
                  <td className={`px-3 py-3 text-right font-semibold ${(trade.estimated_margin ?? 0) < 0 ? "text-red-700" : "text-pipeline"}`}>{money(trade.estimated_margin)}</td>
                  <td className="px-3 py-3"><StatusBadge status={trade.status} /></td>
                  <td className="px-3 py-3">
                    <div className="flex gap-2">
                      <button title="Confirm" className="rounded-md border border-slate-300 p-2 text-blue-700 hover:bg-blue-50" onClick={() => action(trade.id, "confirm")} type="button"><ShieldCheck size={16} /></button>
                      <button title="Settle" className="rounded-md border border-slate-300 p-2 text-emerald-700 hover:bg-emerald-50" onClick={() => action(trade.id, "settle")} type="button"><CheckCircle2 size={16} /></button>
                      <button title="Cancel" className="rounded-md border border-slate-300 p-2 text-red-700 hover:bg-red-50" onClick={() => action(trade.id, "cancel")} type="button"><CircleX size={16} /></button>
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

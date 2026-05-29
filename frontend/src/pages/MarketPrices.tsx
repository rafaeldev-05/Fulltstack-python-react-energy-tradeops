import { FormEvent, useState } from "react";
import { Plus } from "lucide-react";
import { CartesianGrid, Line, LineChart, ResponsiveContainer, Tooltip, XAxis, YAxis } from "recharts";

import { Panel } from "../components/Panel";
import { ErrorBlock, LoadingBlock } from "../components/StateBlock";
import { endpoints } from "../services/api";
import { Commodity, MarketPrice } from "../types/domain";
import { money, percent } from "../utils/format";
import { useAsyncData } from "../hooks/useAsyncData";

export function MarketPrices() {
  const [selectedCommodity, setSelectedCommodity] = useState("");
  const [form, setForm] = useState({
    commodity_id: "",
    reference_date: new Date().toISOString().slice(0, 10),
    price: "",
    currency: "USD",
    source: "MANUAL_DESK_INPUT",
  });

  const { data, loading, error, refresh } = useAsyncData<{ commodities: Commodity[]; prices: MarketPrice[] }>(async () => {
    const commodities = await endpoints.commodities.list();
    const commodityId = selectedCommodity ? Number(selectedCommodity) : commodities[0]?.id;
    const prices = commodityId ? await endpoints.prices.list(commodityId) : [];
    if (!selectedCommodity && commodityId) setSelectedCommodity(String(commodityId));
    return { commodities, prices };
  }, [selectedCommodity]);

  async function submitPrice(event: FormEvent) {
    event.preventDefault();
    await endpoints.prices.create({ ...form, commodity_id: Number(form.commodity_id), price: Number(form.price) });
    setSelectedCommodity(form.commodity_id);
    setForm({ ...form, price: "" });
    refresh();
  }

  if (loading) return <LoadingBlock />;
  if (error || !data) return <ErrorBlock message={error ?? "Market prices unavailable"} />;

  const orderedPrices = [...data.prices].sort((a, b) => a.reference_date.localeCompare(b.reference_date));

  return (
    <div className="space-y-6">
      <Panel title="Register Market Price">
        <form className="grid gap-4 md:grid-cols-5" onSubmit={submitPrice}>
          <select className="rounded-md border border-slate-300 px-3 py-2" required value={form.commodity_id} onChange={(event) => setForm({ ...form, commodity_id: event.target.value })}>
            <option value="">Commodity</option>
            {data.commodities.map((commodity) => <option key={commodity.id} value={commodity.id}>{commodity.name}</option>)}
          </select>
          <input className="rounded-md border border-slate-300 px-3 py-2" type="date" required value={form.reference_date} onChange={(event) => setForm({ ...form, reference_date: event.target.value })} />
          <input className="rounded-md border border-slate-300 px-3 py-2" placeholder="Price" type="number" step="0.01" required value={form.price} onChange={(event) => setForm({ ...form, price: event.target.value })} />
          <input className="rounded-md border border-slate-300 px-3 py-2" placeholder="Source" value={form.source} onChange={(event) => setForm({ ...form, source: event.target.value })} />
          <button className="inline-flex items-center justify-center gap-2 rounded-md bg-market px-4 py-2 font-semibold text-white hover:bg-offshore" type="submit">
            <Plus size={17} />
            Add Price
          </button>
        </form>
      </Panel>

      <Panel
        title="Price History"
        action={
          <select className="rounded-md border border-slate-300 px-3 py-2 text-sm" value={selectedCommodity} onChange={(event) => setSelectedCommodity(event.target.value)}>
            {data.commodities.map((commodity) => <option key={commodity.id} value={commodity.id}>{commodity.symbol}</option>)}
          </select>
        }
      >
        <div className="h-80">
          <ResponsiveContainer>
            <LineChart data={orderedPrices}>
              <CartesianGrid strokeDasharray="3 3" vertical={false} />
              <XAxis dataKey="reference_date" tick={{ fontSize: 11 }} />
              <YAxis tick={{ fontSize: 11 }} domain={["auto", "auto"]} />
              <Tooltip formatter={(value) => money(Number(value))} />
              <Line type="monotone" dataKey="price" stroke="#0E766D" strokeWidth={3} dot={false} />
            </LineChart>
          </ResponsiveContainer>
        </div>
      </Panel>

      <Panel title="Historical Records">
        <div className="table-scroll max-h-[520px] overflow-auto">
          <table className="w-full min-w-[760px] text-left text-sm">
            <thead className="sticky top-0 bg-slate-50 text-xs uppercase text-slate-500">
              <tr>
                <th className="px-3 py-3">Date</th>
                <th className="px-3 py-3 text-right">Price</th>
                <th className="px-3 py-3 text-right">Variation</th>
                <th className="px-3 py-3">Currency</th>
                <th className="px-3 py-3">Source</th>
              </tr>
            </thead>
            <tbody>
              {data.prices.map((price) => (
                <tr key={price.id} className="border-b border-slate-100">
                  <td className="px-3 py-3">{price.reference_date}</td>
                  <td className="px-3 py-3 text-right font-semibold">{money(price.price)}</td>
                  <td className={`px-3 py-3 text-right font-semibold ${price.variation_percent < 0 ? "text-red-700" : "text-pipeline"}`}>{percent(price.variation_percent)}</td>
                  <td className="px-3 py-3">{price.currency}</td>
                  <td className="px-3 py-3">{price.source}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </Panel>
    </div>
  );
}

import { AlertOctagon, Boxes, CircleDollarSign, Clock3, PackageOpen, TrendingUp } from "lucide-react";
import {
  Bar,
  BarChart,
  CartesianGrid,
  Cell,
  Line,
  LineChart,
  Pie,
  PieChart,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
} from "recharts";

import { ErrorBlock, LoadingBlock } from "../components/StateBlock";
import { Panel } from "../components/Panel";
import { StatCard } from "../components/StatCard";
import { endpoints } from "../services/api";
import { RiskAlert, Summary } from "../types/domain";
import { money, number } from "../utils/format";
import { useAsyncData } from "../hooks/useAsyncData";

const palette = ["#2F80ED", "#0E766D", "#F59E0B", "#EF4444", "#64748B", "#7C3AED"];

interface DashboardData {
  summary: Summary;
  volume: Array<{ commodity: string; volume: number }>;
  exposure: Array<{ region: string; exposure: number }>;
  status: Array<{ status: string; count: number }>;
  margins: Array<{ commodity: string; average_margin: number }>;
  alerts: RiskAlert[];
}

export function Dashboard() {
  const { data, loading, error, refresh } = useAsyncData<DashboardData>(async () => {
    const [summary, volume, exposure, status, margins, alerts] = await Promise.all([
      endpoints.analytics.summary(),
      endpoints.analytics.volumeByCommodity(),
      endpoints.analytics.exposureByRegion(),
      endpoints.analytics.tradesByStatus(),
      endpoints.analytics.marginAnalysis(),
      endpoints.alerts.list(),
    ]);
    return { summary, volume, exposure, status, margins, alerts };
  }, []);

  if (loading) return <LoadingBlock />;
  if (error || !data) return <ErrorBlock message={error ?? "Dashboard unavailable"} />;

  const alertSeverity = Object.entries(
    data.alerts.reduce<Record<string, number>>((acc, alert) => {
      acc[alert.severity] = (acc[alert.severity] ?? 0) + 1;
      return acc;
    }, {}),
  ).map(([severity, count]) => ({ severity, count }));

  return (
    <div className="space-y-6">
      <div className="grid gap-4 md:grid-cols-2 xl:grid-cols-3">
        <StatCard label="Financial Exposure" value={money(data.summary.total_financial_exposure)} accent="blue" icon={CircleDollarSign} />
        <StatCard label="Traded Volume" value={number(data.summary.total_traded_volume)} accent="green" icon={Boxes} />
        <StatCard label="Average Margin" value={money(data.summary.average_estimated_margin)} accent="slate" icon={TrendingUp} />
        <StatCard label="Critical Alerts" value={number(data.summary.critical_alerts)} accent="red" icon={AlertOctagon} />
        <StatCard label="Delayed Shipments" value={number(data.summary.delayed_shipments)} accent="amber" icon={Clock3} />
        <StatCard label="Open Operations" value={number(data.summary.open_operations)} accent="slate" icon={PackageOpen} />
      </div>

      <div className="grid gap-6 xl:grid-cols-2">
        <Panel title="Volume by Commodity">
          <div className="h-80">
            <ResponsiveContainer>
              <BarChart data={data.volume}>
                <CartesianGrid strokeDasharray="3 3" vertical={false} />
                <XAxis dataKey="commodity" tick={{ fontSize: 11 }} />
                <YAxis tick={{ fontSize: 11 }} />
                <Tooltip formatter={(value) => number(Number(value))} />
                <Bar dataKey="volume" radius={[4, 4, 0, 0]}>
                  {data.volume.map((_, index) => (
                    <Cell key={index} fill={palette[index % palette.length]} />
                  ))}
                </Bar>
              </BarChart>
            </ResponsiveContainer>
          </div>
        </Panel>

        <Panel title="Exposure by Region">
          <div className="h-80">
            <ResponsiveContainer>
              <BarChart data={data.exposure} layout="vertical" margin={{ left: 20 }}>
                <CartesianGrid strokeDasharray="3 3" horizontal={false} />
                <XAxis type="number" tick={{ fontSize: 11 }} />
                <YAxis dataKey="region" type="category" tick={{ fontSize: 11 }} width={105} />
                <Tooltip formatter={(value) => money(Number(value))} />
                <Bar dataKey="exposure" fill="#0E766D" radius={[0, 4, 4, 0]} />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </Panel>

        <Panel title="Operations by Status">
          <div className="h-72">
            <ResponsiveContainer>
              <PieChart>
                <Pie data={data.status} dataKey="count" nameKey="status" innerRadius={62} outerRadius={96} paddingAngle={3}>
                  {data.status.map((_, index) => (
                    <Cell key={index} fill={palette[index % palette.length]} />
                  ))}
                </Pie>
                <Tooltip />
              </PieChart>
            </ResponsiveContainer>
          </div>
        </Panel>

        <Panel title="Margin by Commodity">
          <div className="h-72">
            <ResponsiveContainer>
              <LineChart data={data.margins}>
                <CartesianGrid strokeDasharray="3 3" vertical={false} />
                <XAxis dataKey="commodity" tick={{ fontSize: 11 }} />
                <YAxis tick={{ fontSize: 11 }} />
                <Tooltip formatter={(value) => money(Number(value))} />
                <Line type="monotone" dataKey="average_margin" stroke="#2F80ED" strokeWidth={3} dot={{ r: 3 }} />
              </LineChart>
            </ResponsiveContainer>
          </div>
        </Panel>

        <Panel title="Alerts by Severity">
          <div className="h-72">
            <ResponsiveContainer>
              <BarChart data={alertSeverity}>
                <CartesianGrid strokeDasharray="3 3" vertical={false} />
                <XAxis dataKey="severity" tick={{ fontSize: 11 }} />
                <YAxis allowDecimals={false} tick={{ fontSize: 11 }} />
                <Tooltip />
                <Bar dataKey="count" fill="#EF4444" radius={[4, 4, 0, 0]} />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </Panel>

        <Panel title="Top Counterparties">
          <div className="space-y-3">
            {data.summary.top_counterparties.map((item, index) => (
              <div key={item.counterparty} className="flex items-center justify-between border-b border-slate-100 pb-3 last:border-0">
                <div className="flex items-center gap-3">
                  <span className="flex h-7 w-7 items-center justify-center rounded-md bg-slate-100 text-sm font-semibold text-slate-600">{index + 1}</span>
                  <span className="font-medium text-ink">{item.counterparty}</span>
                </div>
                <span className="text-sm font-semibold text-pipeline">{number(item.volume)}</span>
              </div>
            ))}
          </div>
        </Panel>
      </div>

      <button className="hidden" type="button" onClick={refresh} aria-hidden="true" />
    </div>
  );
}

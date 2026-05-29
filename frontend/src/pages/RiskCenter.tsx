import { useState } from "react";
import { CheckCircle2 } from "lucide-react";

import { Panel } from "../components/Panel";
import { ErrorBlock, LoadingBlock } from "../components/StateBlock";
import { StatusBadge } from "../components/StatusBadge";
import { endpoints } from "../services/api";
import { RiskSeverity } from "../types/domain";
import { useAsyncData } from "../hooks/useAsyncData";

const severities: RiskSeverity[] = ["LOW", "MEDIUM", "HIGH", "CRITICAL"];

export function RiskCenter() {
  const [severity, setSeverity] = useState("");
  const { data, loading, error, refresh } = useAsyncData(async () => endpoints.alerts.list(severity ? (severity as RiskSeverity) : undefined), [severity]);

  async function resolve(id: number) {
    await endpoints.alerts.resolve(id);
    refresh();
  }

  if (loading) return <LoadingBlock />;
  if (error || !data) return <ErrorBlock message={error ?? "Risk alerts unavailable"} />;

  return (
    <Panel
      title="Risk Alerts"
      action={
        <select className="rounded-md border border-slate-300 px-3 py-2 text-sm" value={severity} onChange={(event) => setSeverity(event.target.value)}>
          <option value="">All severities</option>
          {severities.map((item) => <option key={item}>{item}</option>)}
        </select>
      }
    >
      <div className="grid gap-4">
        {data.map((alert) => (
          <article key={alert.id} className="rounded-lg border border-slate-200 bg-white p-4 shadow-sm">
            <div className="flex flex-col gap-3 md:flex-row md:items-start md:justify-between">
              <div>
                <div className="flex flex-wrap items-center gap-2">
                  <StatusBadge status={alert.severity} />
                  {alert.related_trade_id ? <span className="rounded-md bg-slate-100 px-2.5 py-1 text-xs font-semibold text-slate-600">Trade {alert.related_trade_id}</span> : null}
                </div>
                <h3 className="mt-3 text-base font-semibold text-ink">{alert.title}</h3>
                <p className="mt-1 text-sm leading-6 text-slate-600">{alert.description}</p>
                <div className="mt-2 text-xs text-slate-500">{new Date(alert.created_at).toLocaleString()}</div>
              </div>
              <button className="inline-flex items-center justify-center gap-2 rounded-md border border-emerald-300 px-3 py-2 text-sm font-semibold text-emerald-700 hover:bg-emerald-50" onClick={() => resolve(alert.id)} type="button">
                <CheckCircle2 size={16} />
                Resolve
              </button>
            </div>
          </article>
        ))}
      </div>
    </Panel>
  );
}

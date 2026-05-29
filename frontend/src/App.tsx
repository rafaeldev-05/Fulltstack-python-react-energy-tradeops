import { useState } from "react";

import { Header } from "./components/Header";
import { PageKey, Sidebar } from "./components/Sidebar";
import { Dashboard } from "./pages/Dashboard";
import { Logistics } from "./pages/Logistics";
import { MarketPrices } from "./pages/MarketPrices";
import { RiskCenter } from "./pages/RiskCenter";
import { TradeOperations } from "./pages/TradeOperations";

const titles: Record<PageKey, string> = {
  dashboard: "Executive Dashboard",
  trades: "Trade Operations",
  prices: "Market Prices",
  logistics: "Logistics Control",
  risk: "Risk Center",
};

export default function App() {
  const [page, setPage] = useState<PageKey>("dashboard");

  return (
    <div className="min-h-screen bg-slate-100">
      <Sidebar activePage={page} onChange={setPage} />
      <div className="lg:pl-72">
        <div className="lg:hidden">
          <div className="bg-ink px-4 py-4 text-white">
            <div className="text-xs font-semibold uppercase tracking-[0.22em] text-emerald-300">Energy</div>
            <div className="text-lg font-semibold">TradeOps Platform</div>
          </div>
          <div className="grid grid-cols-2 gap-2 border-b border-slate-200 bg-white p-2 sm:grid-cols-5">
            {(["dashboard", "trades", "prices", "logistics", "risk"] as PageKey[]).map((item) => (
              <button
                key={item}
                className={`rounded-md px-3 py-2 text-sm font-semibold ${page === item ? "bg-ink text-white" : "bg-slate-100 text-slate-700"}`}
                onClick={() => setPage(item)}
                type="button"
              >
                {titles[item].replace("Executive ", "").replace(" Control", "")}
              </button>
            ))}
          </div>
        </div>
        <Header title={titles[page]} />
        <main className="px-4 py-6 lg:px-8">
          {page === "dashboard" && <Dashboard />}
          {page === "trades" && <TradeOperations />}
          {page === "prices" && <MarketPrices />}
          {page === "logistics" && <Logistics />}
          {page === "risk" && <RiskCenter />}
        </main>
      </div>
    </div>
  );
}

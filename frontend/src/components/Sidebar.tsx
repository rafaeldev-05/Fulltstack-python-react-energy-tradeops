import { AlertTriangle, BarChart3, Gauge, Ship, TrendingUp } from "lucide-react";

export type PageKey = "dashboard" | "trades" | "prices" | "logistics" | "risk";

const navItems = [
  { key: "dashboard" as PageKey, label: "Dashboard", icon: Gauge },
  { key: "trades" as PageKey, label: "Trade Operations", icon: TrendingUp },
  { key: "prices" as PageKey, label: "Market Prices", icon: BarChart3 },
  { key: "logistics" as PageKey, label: "Logistics", icon: Ship },
  { key: "risk" as PageKey, label: "Risk Center", icon: AlertTriangle },
];

interface SidebarProps {
  activePage: PageKey;
  onChange: (page: PageKey) => void;
}

export function Sidebar({ activePage, onChange }: SidebarProps) {
  return (
    <aside className="fixed inset-y-0 left-0 z-20 hidden w-72 border-r border-slate-200 bg-ink text-white lg:block">
      <div className="border-b border-white/10 px-6 py-6">
        <div className="text-xs font-semibold uppercase tracking-[0.22em] text-emerald-300">Energy</div>
        <div className="mt-1 text-xl font-semibold">TradeOps Platform</div>
      </div>
      <nav className="space-y-2 px-4 py-5">
        {navItems.map((item) => {
          const Icon = item.icon;
          const active = activePage === item.key;
          return (
            <button
              key={item.key}
              className={`flex w-full items-center gap-3 rounded-md px-4 py-3 text-left text-sm font-medium transition ${
                active ? "bg-white text-ink shadow-executive" : "text-slate-300 hover:bg-white/10 hover:text-white"
              }`}
              onClick={() => onChange(item.key)}
              type="button"
            >
              <Icon size={18} />
              {item.label}
            </button>
          );
        })}
      </nav>
      <div className="absolute bottom-0 left-0 right-0 border-t border-white/10 px-6 py-5 text-xs text-slate-400">
        Trading, supply chain, analytics and risk control.
      </div>
    </aside>
  );
}

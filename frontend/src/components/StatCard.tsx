import { LucideIcon } from "lucide-react";

interface StatCardProps {
  label: string;
  value: string;
  accent: "blue" | "green" | "amber" | "red" | "slate";
  icon: LucideIcon;
}

const accents = {
  blue: "bg-blue-50 text-market",
  green: "bg-emerald-50 text-pipeline",
  amber: "bg-amber-50 text-amber-700",
  red: "bg-red-50 text-red-700",
  slate: "bg-slate-100 text-slate-700",
};

export function StatCard({ label, value, accent, icon: Icon }: StatCardProps) {
  return (
    <section className="rounded-lg border border-slate-200 bg-white p-5 shadow-executive">
      <div className="flex items-start justify-between gap-3">
        <div>
          <div className="text-sm font-medium text-slate-500">{label}</div>
          <div className="mt-2 text-2xl font-semibold text-ink">{value}</div>
        </div>
        <div className={`rounded-md p-2 ${accents[accent]}`}>
          <Icon size={20} />
        </div>
      </div>
    </section>
  );
}

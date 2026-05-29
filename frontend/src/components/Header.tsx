import { Activity, RefreshCw } from "lucide-react";

interface HeaderProps {
  title: string;
  onRefresh?: () => void;
}

export function Header({ title, onRefresh }: HeaderProps) {
  return (
    <header className="sticky top-0 z-10 border-b border-slate-200 bg-white/95 px-4 py-4 backdrop-blur lg:px-8">
      <div className="flex flex-col gap-3 sm:flex-row sm:items-center sm:justify-between">
        <div>
          <div className="flex items-center gap-2 text-xs font-semibold uppercase tracking-[0.2em] text-pipeline">
            <Activity size={15} />
            Live Operations
          </div>
          <h1 className="mt-1 text-2xl font-semibold text-ink">{title}</h1>
        </div>
        {onRefresh ? (
          <button
            className="inline-flex items-center justify-center gap-2 rounded-md border border-slate-300 bg-white px-4 py-2 text-sm font-semibold text-ink hover:border-market hover:text-market"
            onClick={onRefresh}
            type="button"
          >
            <RefreshCw size={16} />
            Refresh
          </button>
        ) : null}
      </div>
    </header>
  );
}

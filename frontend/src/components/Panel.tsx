import { ReactNode } from "react";

interface PanelProps {
  title: string;
  children: ReactNode;
  action?: ReactNode;
}

export function Panel({ title, children, action }: PanelProps) {
  return (
    <section className="rounded-lg border border-slate-200 bg-white shadow-executive">
      <div className="flex items-center justify-between gap-3 border-b border-slate-200 px-5 py-4">
        <h2 className="text-base font-semibold text-ink">{title}</h2>
        {action}
      </div>
      <div className="p-5">{children}</div>
    </section>
  );
}

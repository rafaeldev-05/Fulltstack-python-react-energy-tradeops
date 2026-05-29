export function LoadingBlock() {
  return <div className="rounded-md border border-slate-200 bg-white p-6 text-sm text-slate-500">Loading data...</div>;
}

export function ErrorBlock({ message }: { message: string }) {
  return <div className="rounded-md border border-red-200 bg-red-50 p-4 text-sm font-medium text-red-700">{message}</div>;
}

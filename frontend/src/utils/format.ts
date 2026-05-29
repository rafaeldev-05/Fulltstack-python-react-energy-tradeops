export function money(value?: number | null) {
  return new Intl.NumberFormat("en-US", {
    style: "currency",
    currency: "USD",
    maximumFractionDigits: 0,
  }).format(value ?? 0);
}

export function number(value?: number | null) {
  return new Intl.NumberFormat("en-US", { maximumFractionDigits: 2 }).format(value ?? 0);
}

export function percent(value?: number | null) {
  return `${number(value)}%`;
}

# Energy TradeOps Frontend

A React and TypeScript single-page application built with Vite, Tailwind CSS, Axios, Recharts, and Lucide.

## Run locally

From the repository root:

```sh
cd frontend
npm install
npm run dev
```

Open http://localhost:5173. Start the backend separately so the UI can load data.

The frontend uses `http://localhost:8000/api/v1` by default. To use another API address, set `VITE_API_BASE_URL` in a `.env.local` file in this directory.

Run `npm run build` to type-check the code and create a production build.

## Screens

- Executive Dashboard
- Trade Operations
- Market Prices
- Logistics
- Risk Center

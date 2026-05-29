/** @type {import('tailwindcss').Config} */
export default {
  content: ["./index.html", "./src/**/*.{ts,tsx}"],
  theme: {
    extend: {
      colors: {
        ink: "#102033",
        offshore: "#0F3D4E",
        pipeline: "#0E766D",
        market: "#2F80ED",
        steel: "#64748B",
      },
      boxShadow: {
        executive: "0 14px 36px rgba(15, 45, 62, 0.12)",
      },
    },
  },
  plugins: [],
};

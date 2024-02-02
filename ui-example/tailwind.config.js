/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{vue,js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        "app-bg": "#2E2F39",
        "app-text": "#D1D5DB",
        "app-border": "#4F505A",
        success: {
          500: "#396249",
          700: "#0FD75C",
        },
        error: "#ff0000",
      },
    },
  },
  plugins: [],
}


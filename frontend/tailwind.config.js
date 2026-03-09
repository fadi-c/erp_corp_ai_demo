/** @type {import('tailwindcss').Config} */

module.exports = {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}"
  ],

  darkMode: "class",

  theme: {
    extend: {

      colors: {

        background: "#020617",
        surface: "#0f172a",
        panel: "#1e293b",

        accent: {
          DEFAULT: "#6366f1",
          hover: "#4f46e5"
        },

        assistant: "#334155"

      },

      fontFamily: {
        sans: ["Inter", "ui-sans-serif", "system-ui"]
      },

      borderRadius: {
        xl: "1rem",
        "2xl": "1.25rem",
        "3xl": "1.75rem"
      },

      boxShadow: {
        glow: "0 0 20px rgba(99,102,241,0.4)",
        soft: "0 10px 30px rgba(0,0,0,0.25)"
      }

    }
  },

  plugins: [
    require("@tailwindcss/typography")
  ]
}
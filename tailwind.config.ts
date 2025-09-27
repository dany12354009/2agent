import type { Config } from "tailwindcss";

const config: Config = {
  darkMode: "class",
  content: [
    "./app/**/*.{ts,tsx}",
    "./components/**/*.{ts,tsx}",
    "./lib/**/*.{ts,tsx}"
  ],
  theme: {
    extend: {
      colors: {
        background: "#0B0F12",
        surface: "#0F141A",
        accent: "#15C2B8",
        text: {
          DEFAULT: "#E6ECEF",
          muted: "#9FB2BF"
        },
        border: "#1B232C"
      },
      fontFamily: {
        sans: ["Inter", "ui-sans-serif", "system-ui"],
        mono: ["'JetBrains Mono'", "ui-monospace", "SFMono-Regular"]
      },
      boxShadow: {
        glass: "0 24px 48px -32px rgba(11, 15, 18, 0.9)",
        subtle: "0 12px 32px -20px rgba(21, 194, 184, 0.2)"
      },
      borderRadius: {
        xl: "16px"
      },
      keyframes: {
        pulseGlow: {
          "0%, 100%": { opacity: '0.7' },
          "50%": { opacity: '1' }
        }
      },
      animation: {
        pulseGlow: "pulseGlow 4s ease-in-out infinite"
      }
    }
  },
  plugins: []
};

export default config;

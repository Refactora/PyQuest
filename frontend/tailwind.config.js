/** @type {import('tailwindcss').Config} */
export default {
  content: ['./index.html', './src/**/*.{js,ts,jsx,tsx}'],
  theme: {
    extend: {
      fontFamily: {
        mono: ['JetBrains Mono', 'Fira Code', 'monospace'],
      },
      animation: {
        'hp-flash': 'hp-flash 0.3s ease-in-out',
        'xp-gain': 'xp-gain 0.6s ease-out',
      },
      keyframes: {
        'hp-flash': {
          '0%, 100%': { opacity: '1' },
          '50%': { opacity: '0.3', backgroundColor: '#ef4444' },
        },
        'xp-gain': {
          '0%': { transform: 'scale(1)' },
          '50%': { transform: 'scale(1.1)', color: '#fbbf24' },
          '100%': { transform: 'scale(1)' },
        },
      },
    },
  },
  plugins: [],
}

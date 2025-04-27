/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './pages/**/*.{js,ts,jsx,tsx,mdx}',
    './components/**/*.{js,ts,jsx,tsx,mdx}',
    './src/**/*.{js,ts,jsx,tsx,mdx}',
  ],
  theme: {
    extend: {
      colors: {
        'orange': '#FF5500',
        'blood-red': '#8A0303',
        'dark-purple': '#1A0933',
      },
      fontFamily: {
        'bebas': ['Bebas Neue', 'sans-serif'],
      },
      backgroundImage: {
        'gradient-radial': 'radial-gradient(var(--tw-gradient-stops))',
      },
      animation: {
        'fiery-pulse': 'fiery-pulse 2s infinite',
        'pulse-glow': 'pulse-glow 3s infinite',
        'flame-dance': 'flame-dance 4s infinite',
        'smoke-float': 'smoke-float 3s infinite',
      },
      keyframes: {
        'fiery-pulse': {
          '0%, 100%': { boxShadow: '0 0 0 0 rgba(255, 85, 0, 0.7)' },
          '50%': { boxShadow: '0 0 20px 5px rgba(255, 85, 0, 0.4)' },
        },
        'pulse-glow': {
          '0%, 100%': { filter: 'brightness(1)' },
          '50%': { filter: 'brightness(1.3)' },
        },
        'flame-dance': {
          '0%, 100%': { transform: 'rotate(-2deg) scale(1)' },
          '25%': { transform: 'rotate(2deg) scale(1.05)' },
          '50%': { transform: 'rotate(-1deg) scale(1.02)' },
          '75%': { transform: 'rotate(1deg) scale(1.03)' },
        },
        'smoke-float': {
          '0%': { transform: 'translateY(0) scale(1)' },
          '50%': { transform: 'translateY(-10px) scale(1.03)' },
          '100%': { transform: 'translateY(0) scale(1)' },
        },
      },
    },
  },
  plugins: [],
};
/** @type {import('tailwindcss').Config} */
module.exports = {
  darkMode: 'class',
  content: [
    './pages/**/*.{js,ts,jsx,tsx,mdx}',
    './components/**/*.{js,ts,jsx,tsx,mdx}',
    './app/**/*.{js,ts,jsx,tsx,mdx}',
    './src/**/*.{js,ts,jsx,tsx,mdx}',
  ],
  theme: {
    extend: {
      colors: {
        surface: {
          base: '#FFFFFF',
        },
        badge: {
          DEFAULT: '#F3F4F4',
          subtle: '#F8F9FA',
        },
        text: {
          primary: '#3A3E42',
          muted: '#6B7280',
        },
        neutral: {
          black: '#000000',
        },
        apple: {
          border: 'rgba(0, 0, 0, 0.08)',
          borderHover: 'rgba(0, 0, 0, 0.16)',
          glass: 'rgba(255, 255, 255, 0.85)',
          shadow: '0 4px 24px -2px rgba(0, 0, 0, 0.06)',
        }
      },
      fontFamily: {
        sans: [
          '"Inter Display"',
          '"Inter"',
          '-apple-system',
          'BlinkMacSystemFont',
          'system-ui',
          'sans-serif',
        ],
        mono: [
          '"SF Mono"',
          '"JetBrains Mono"',
          'monospace',
        ],
      },
      fontWeight: {
        regular: '400',
        medium: '500',
      },
      letterSpacing: {
        tight: '-0.015em',
        tighter: '-0.025em',
      },
      transitionTimingFunction: {
        apple: 'cubic-bezier(0.16, 1, 0.3, 1)',
      },
    },
  },
  plugins: [],
}

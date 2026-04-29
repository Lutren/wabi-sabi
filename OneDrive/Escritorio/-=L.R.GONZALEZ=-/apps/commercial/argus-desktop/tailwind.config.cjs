/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ['./index.html', './src/**/*.{ts,tsx}'],
  theme: {
    extend: {
      boxShadow: {
        aura: '0 30px 80px rgba(0, 0, 0, 0.45)',
        glass: '0 18px 50px rgba(0, 0, 0, 0.35)'
      },
      transitionTimingFunction: {
        observatory: 'cubic-bezier(0.23, 1, 0.32, 1)'
      }
    }
  },
  plugins: []
}

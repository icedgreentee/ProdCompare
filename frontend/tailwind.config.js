/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./src/**/*.{js,jsx,ts,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        'sephora-pink': '#E40046',
        'nykaa-pink': '#FF6B9D',
      }
    },
  },
  plugins: [],
}


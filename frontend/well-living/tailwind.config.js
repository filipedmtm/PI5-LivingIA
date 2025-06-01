/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{vue,js,ts,jsx,tsx}", // ESSENCIAL para Tailwind funcionar no Vue
  ],
  theme: {
    extend: {
      colors: {
        teal: {
          800: '#035C67',
        },
        amber: {
          50: '#F6E9DC',
        },
      },
      fontFamily: {
        sans: ['Manrope', 'ui-sans-serif', 'system-ui'], // seta Manrope como fonte padrão sans
      },
    },
  },
  plugins: [],
}

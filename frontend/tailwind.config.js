/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ['./index.html', './src/**/*.{js,ts,jsx,tsx}'],
  theme: {
    extend: {
      colors: {
        primary: {
          DEFAULT: '#283618'
        },
        secondary: {
          DEFAULT: '#B7B7A4'
        },
        accent: {
          DEFAULT: '#D4D4D4'
        },
        neutral: {
          DEFAULT: '#F0EFEB'
        }
      },
      keyframes: {
        spinSlow: {
          from: { transform: 'rotate(0deg)' },
          to: { transform: 'rotate(360deg)' },
        },
      },
      animation: {
        spinSlow: 'spinSlow 3s linear infinite',
      },
    },
  },
  plugins: [
    require('@tailwindcss/typography'),
  ],
};

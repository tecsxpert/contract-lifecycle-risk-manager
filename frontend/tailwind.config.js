/** @type {import('tailwindcss').Config} */
export default {
    content: [
        "./index.html",
        "./src/**/*.{js,ts,jsx,tsx}",
    ],
    theme: {
        extend: {
            colors: {
                // Set the Primary Brand Color
                primary: '#1B4F8A',
            },
            fontFamily: {
                // Set the Brand Font
                sans: ['Arial', 'sans-serif'],
            },
            spacing: {
                // Reinforce the 8px grid (1 unit = 4px in Tailwind, so 2 units = 8px)
                '8px': '8px',
            },
        },
    },
    plugins: [],
}
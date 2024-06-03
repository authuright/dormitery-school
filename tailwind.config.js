/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./apps/templates/**/*.{html,htm}",
    "./apps/static/**/*.js",
    "./node_modules/flowbite/**/*.js"
  ],
  theme: {
    extend: {},
  },
  plugins: [
    require("flowbite/plugin")
  ],
}


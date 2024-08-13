import type { Config } from 'tailwindcss'

const config: Config = {
  content: [
    './app/**/*.{js,ts,jsx,tsx,mdx}',
    './pages/**/*.{js,ts,jsx,tsx,mdx}',
    './components/**/*.{js,ts,jsx,tsx,mdx}',

    // Or if using `src` directory:
    './src/**/*.{js,ts,jsx,tsx,mdx}',
  ],
  theme: {
    extend: {
      colors: {
        'basic-0': '#000000',
        'basic-1': '#F7FAFC',
        'basic-2': '#EFF2F4',
        'basic-3': '#DEE2E7',
        'basic-4': '#BDC4CD',
        'basic-5': '#8B96A5',
        'basic-6': '#1C1C1C',
        'white': '#ffffff',
        'red-light': '#FFE0E0',
        'red-bold': '#FA3434',
        'green-light': '#E5F7E7',
        'green-bold': '#00B517',
        'orange-light': '#FFF3E7',
        'orange-bold': '#FF9017',
        'blue-bold': '#127FFF',
      },
      fontFamily: {
        'roboto': ['Roboto'],
      },
      width: {
        container: '1200px',
      },
      fontSize: {
        48: '48px',
        32: '32px',
        24: '24px',
        20: '20px',
        18: '18px',
        16: '16px',
        13: '13px',
      },
      borderRadius: {
        10: '10px',
        5: '5px',
        3: '3px',
      },
    },
  },
  plugins: [],
  corePlugins: {
    preflight: true, // <== enable this, default!
  },
}
export default config

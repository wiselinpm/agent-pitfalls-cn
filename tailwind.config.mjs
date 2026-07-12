/** @type {import('tailwindcss').Config} */
export default {
  content: ['./web/src/**/*.{astro,html,js,jsx,md,mdx,svelte,ts,tsx,vue}'],
  // SST — Style Reference: light theme only
  // Two-font system: Rubik Variable for prose, IBM Plex Mono for code/technical
  theme: {
    extend: {
      colors: {
        ink: {
          DEFAULT: '#303055',
          50: '#f7f7fa',
          100: '#e8e8f2',
          200: '#d8d8e3',
          300: '#b3b3c8',
          400: '#8585a0',
          500: '#5e5e7d',
          600: '#484866',
          700: '#303055',
          800: '#232342',
          900: '#111122',
        },
        plum: { DEFAULT: '#8844ae' },
        cobalt: { DEFAULT: '#3b61b0' },
        teal: { DEFAULT: '#096e72' },
        rust: { DEFAULT: '#984e4d' },
        slate: { DEFAULT: '#403f53' },
        fog: { DEFAULT: '#767682' },
        mist: { DEFAULT: '#a8a8b0' },
        obsidian: { DEFAULT: '#111111' },
        paper: '#ffffff',
        'lavender-mist': '#e8e8f2',
      },
      fontFamily: {
        sans: ['Rubik Variable', 'Rubik', 'Inter', 'PingFang SC', 'Microsoft YaHei', 'system-ui', 'sans-serif'],
        mono: ['IBM Plex Mono', 'JetBrains Mono', 'Fira Code', 'ui-monospace', 'SFMono-Regular', 'Menlo', 'Monaco', 'Consolas', 'monospace'],
      },
      fontSize: {
        caption: ['12px', { lineHeight: '1.5' }],
        body: ['14px', { lineHeight: '1.8' }],
        'heading-sm': ['18px', { lineHeight: '1.5' }],
        heading: ['20px', { lineHeight: '1.5' }],
        display: ['48px', { lineHeight: '1.1', letterSpacing: '-1.01px' }],
      },
      spacing: {
        'section-gap': '64px',
      },
      maxWidth: {
        page: '1200px',
      },
      borderRadius: {
        sm: '1px',
        md: '4px',
        lg: '8px',
      },
      boxShadow: {
        code: '0 0 0 1px rgba(0,0,0,0.04), 0 4px 12px rgba(0,0,0,0.04)',
        hairline: '0 0 0 1px rgba(0,0,0,0.04)',
      },
      typography: {
        DEFAULT: {
          css: {
            'code::before': { content: '""' },
            'code::after': { content: '""' },
          },
        },
      },
    },
  },
  plugins: [require('@tailwindcss/typography')],
};
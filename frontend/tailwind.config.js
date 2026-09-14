/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        // Background layers
        'bg-primary': '#FFFFFF',
        'bg-secondary': '#F8F9FA',
        'bg-tertiary': '#F1F3F5',
        
        // Text colors
        'text-primary': '#1A1D1F',
        'text-secondary': '#6C7380',
        'text-tertiary': '#9FA4AD',
        
        // Border colors
        'border-primary': '#E5E7EB',
        'border-secondary': '#F1F3F5',
        'border-focus': '#3B82F6',
        
        // Surface colors
        'surface-base': '#FFFFFF',
        'surface-hover': '#F8F9FA',
        'surface-active': '#F1F3F5',
        
        // Accent colors
        'primary': '#2563EB',
        'primary-hover': '#1D4ED8',
        'primary-active': '#1E40AF',
        
        // Source citation accent
        'source-bg': '#FEF3C7',
        'source-border': '#F59E0B',
        'source-text': '#92400E',
        
        // AI message accent
        'ai-bg': '#F0F9FF',
        'ai-border': '#BFDBFE',
      },
      spacing: {
        '1': '4px',
        '2': '8px',
        '3': '12px',
        '4': '16px',
        '5': '20px',
        '6': '24px',
        '8': '32px',
        '10': '40px',
        '12': '48px',
        '16': '64px',
      },
      fontSize: {
        'display': ['32px', '40px'],
        'headline': ['20px', '28px'],
        'body': ['15px', '24px'],
        'small': ['13px', '20px'],
        'tiny': ['11px', '16px'],
      },
    },
  },
  plugins: [],
}

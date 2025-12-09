/**
 * plugins/vuetify.js
 *
 * Framework documentation: https://vuetifyjs.com`
 */

// Styles
import '@mdi/font/css/materialdesignicons.css'
import 'vuetify/styles'
import * as components from 'vuetify/components';
import * as directives from 'vuetify/directives';
// Composables
import { createVuetify } from 'vuetify'

// https://vuetifyjs.com/en/introduction/why-vuetify/#feature-guides
export default createVuetify({
  components,
  directives,
  theme: {
    defaultTheme: 'light',
    themes: {
      light: {
        dark: false,
        colors: {
          background: '#F8FAFC',
          surface: '#FFFFFF',
          primary: '#2563EB',
          secondary: '#475569',
          error: '#EF4444',
          info: '#3B82F6',
          success: '#10B981',
          warning: '#F59E0B',
        },
      },
      dark: {
        dark: true,
        colors: {
          background: '#0F172A',
          surface: '#1E293B',
          primary: '#3B82F6',
          secondary: '#94A3B8',
          error: '#F87171',
          info: '#60A5FA',
          success: '#34D399',
          warning: '#FBBF24',
        },
      },
    },
  },
  defaults: {
    global: {
      ripple: false,
    },
    VBtn: {
      variant: 'flat',
      height: 44,
      class: 'text-none font-weight-bold rounded-lg',
      elevation: 0,
    },
    VCard: {
      elevation: 0,
      border: 'thin',
      class: 'rounded-xl',
    },
    VTextField: {
      variant: 'outlined',
      color: 'primary',
      density: 'comfortable',
      class: 'rounded-lg',
      hideDetails: 'auto',
    },
  },
});



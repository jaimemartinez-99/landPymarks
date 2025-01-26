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
    defaultTheme: 'dark', // Tema oscuro por defecto
    themes: {
      dark: {
        dark: true, // Activa el tema oscuro
        colors: {
          background: '#3f415b6e', // Fondo semitransparente
          surface: '#2c2d3d', // Color de superficie para tarjetas y contenedores
          primary: '#1976d2', // Color primario
          secondary: '#424242', // Color secundario
          error: '#ff4444', // Color de error
          info: '#33b5e5', // Color de información
          success: '#00c851', // Color de éxito
          warning: '#ffbb33', // Color de advertencia
        },
      },
    },
  },
});



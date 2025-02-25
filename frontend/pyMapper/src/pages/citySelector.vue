<template>
  <v-container class="city-selector-container">
    <v-row justify="center" align="center">
      <v-col cols="12" md="6">
        <v-card class="pa-6" elevation="10">
          <v-card-title class="text-h3 font-weight-bold text-center mb-6 text-primary">
            Plan Your Trip
          </v-card-title>
          <v-card-subtitle class="text-h6 text-center mb-8 text-secondary">
            Enter your destination and the number of days to generate an optimized route.
          </v-card-subtitle>
          <v-form @submit.prevent="generateRoute">
            <v-text-field
              v-model="city"
              label="City"
              required
              outlined
              placeholder="Enter a city"
              prepend-inner-icon="mdi-city"
              class="mb-4"
              background-color="surface"
              :disabled="loading"
            ></v-text-field>

            <v-text-field
              v-model="numberOfDays"
              label="Number of Days"
              type="number"
              required
              outlined
              placeholder="Enter number of days"
              prepend-inner-icon="mdi-calendar"
              class="mb-6"
              background-color="surface"
              :disabled="loading"
            ></v-text-field>

            <v-btn
              type="submit"
              color="primary"
              size="large"
              block
              @click="generateRoute"
              :disabled="loading"
            >
              <span v-if="!loading">Generate Route</span>
              <span v-else>
                Generating...
                <v-progress-circular
                  indeterminate
                  color="white"
                  size="24"
                  class="ml-2"
                ></v-progress-circular>
              </span>
            </v-btn>
          </v-form>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script setup>
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import axios from 'axios';

const city = ref('');
const numberOfDays = ref(0);
const loading = ref(false); // Estado para controlar el loader
const router = useRouter();

const generateRoute = async () => {
  loading.value = true; // Activar el loader
  console.log('Generating route...'); // Log de inicio

  const url = `https://landpymarks.onrender.com/generar-ruta/?ciudad=${encodeURIComponent(city.value)}&num_dias=${parseInt(numberOfDays.value)}`;
  try {
    console.log('Sending request to backend...'); // Log de la solicitud
    const response = await axios.post(url, null, {
      headers: {
        'Content-Type': 'application/json', // Opcional, dependiendo del backend
      },
    });

    console.log('Response from backend:', response.data); // Log de la respuesta

    localStorage.setItem('mapas', JSON.stringify(response.data.mapas));
    console.log('Maps saved to localStorage.'); // Log de guardado en localStorage

    router.push('/maps');
  } catch (error) {
    console.error('Error generating route:', error); // Log de error
    alert('Error generating route. Please try again.');
  } finally {
    loading.value = false; // Desactivar el loader
    console.log('Request completed.'); // Log de finalización
  }
};
</script>

<style scoped>
.city-selector-container {
  padding-top: 100px;
  padding-bottom: 100px;
  min-height: 100vh; /* Asegura que el fondo cubra toda la pantalla */
  display: flex;
  align-items: center;
  justify-content: center;
}

.text-primary {
  color: #1976d2 !important; /* Color primario de Vuetify */
}

.text-secondary {
  color: #424242 !important; /* Color secundario de Vuetify */
}
</style>
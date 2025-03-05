<template>
  <v-container class="city-selector-container">
    <v-row justify="center" align="center">
      <v-col cols="12" sm="8" md="6">
        <v-card class="pa-3 pa-sm-4" elevation="10">
          <!-- Title -->
          <v-card-title class="text-h5 text-sm-h4 font-weight-bold text-center mb-3 mb-sm-4 text-primary">
            Plan Your Trip
          </v-card-title>

          <!-- Subtitle -->
          <v-card-subtitle class="text-caption text-sm-subtitle-1 text-center mb-3 mb-sm-4 text-secondary">
            Enter your destination and the number of days to generate an optimized route.
          </v-card-subtitle>

          <!-- Form -->
          <v-form @submit.prevent="generateRoute">
            <!-- City Input -->
            <v-text-field
              v-model="city"
              label="City"
              required
              outlined
              dense
              placeholder="Enter a city"
              prepend-inner-icon="mdi-city"
              class="mb-3"
              background-color="surface"
              :disabled="loading"
            ></v-text-field>

            <!-- Number of Days Input -->
            <v-text-field
              v-model="numberOfDays"
              label="Number of Days"
              type="number"
              required
              outlined
              dense
              placeholder="Enter number of days"
              prepend-inner-icon="mdi-calendar"
              class="mb-3 mb-sm-4"
              background-color="surface"
              :disabled="loading"
            ></v-text-field>

            <!-- Generate Route Button -->
            <v-btn
              type="submit"
              color="primary"
              size="default"
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
                  size="20"
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

  const url = `https://landpymarks.onrender.comgenerar-ruta/?ciudad=${encodeURIComponent(city.value)}&num_dias=${parseInt(numberOfDays.value)}`;
  try {
    const response = await axios.post(url, null, {
      headers: {
        'Content-Type': 'application/json', // Opcional, dependiendo del backend
      },
    });

    const uuid = response.data.link;

    localStorage.setItem(response.data.link, JSON.stringify(response.data.mapas));
    localStorage.setItem('ciudad', city.value);
    localStorage.setItem('num_dias', numberOfDays.value);

    router.push({ path: `/${uuid}` }); // Use the route name and pass the UUID
    } catch (error) {
    console.error('Error generating route:', error); // Log de error
    alert('Error generating route. Please try again.');
  } finally {
    loading.value = false; // Desactivar el loader
  }
};
</script>

<style scoped>
.city-selector-container {
  padding-top: 20px;
  padding-bottom: 20px;
  min-height: 100vh; /* Asegura que el fondo cubra toda la pantalla */
  display: flex;
  align-items: center;
  justify-content: center;
}

.text-primary {
  color: #1976d2 !important; /* Color primario de Vuetify */
}

.text-secondary {
  color: #ffffff !important; /* Color secundario de Vuetify */
}

/* Adjustments for mobile devices */
@media (max-width: 600px) {
  .city-selector-container {
    padding-top: 10px;
    padding-bottom: 10px;
    min-height: 100vh;
  }

  .v-card {
    padding: 12px !important; /* Smaller padding for mobile */
  }

  .v-card-title {
    font-size: 1.25rem !important; /* Smaller font size for mobile */
    line-height: 1.2; /* Adjust line height for better readability */
  }

  .v-card-subtitle {
    font-size: 0.75rem !important; /* Smaller font size for mobile */
    line-height: 1.3; /* Adjust line height for better readability */
  }

  .v-text-field {
    font-size: 0.875rem !important; /* Smaller font size for input fields */
  }

  .v-btn {
    font-size: 0.875rem !important; /* Smaller font size for button */
    padding: 6px 12px !important; /* Adjust button padding */
  }
}
</style>
<template>
  <v-container class="maps-container">
    <v-row justify="center">
      <v-col cols="12" md="8">
        <v-card class="pa-6" elevation="10">
          <v-card-title class="text-h3 font-weight-bold text-center mb-6 text-primary">
            Generated Maps
          </v-card-title>
          <v-card-subtitle class="text-h6 text-center mb-8 text-secondary">
            Explore the optimized routes for your trip.
          </v-card-subtitle>
          <v-card-subtitle class="text-h6 text-center mb-8 text-secondary">
            Beware the maps are not real, they are just a representation of the optimized routes and exact locations may vary from the representation
          </v-card-subtitle>

          <!-- Mostrar los mapas generados -->
          <div v-for="(mapa, index) in mapas" :key="index" class="mb-6">
            <v-card>
              <v-card-title class="text-h5 font-weight-bold">
                Day {{ index + 1 }}
              </v-card-title>
              <v-card-text>
                <div v-html="mapa"></div> <!-- Renderizar el mapa -->
              </v-card-text>
            </v-card>
          </div>

          <!-- Botón para regresar -->
          <v-btn
            color="primary"
            size="large"
            block
            @click="goBack"
          >
            Go Back
          </v-btn>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { useRouter } from 'vue-router';

const mapas = ref([]); // Array para almacenar los mapas
const router = useRouter();

// Obtener los mapas desde localStorage
onMounted(() => {
  const mapasGuardados = localStorage.getItem('mapas');
  if (mapasGuardados) {
    mapas.value = JSON.parse(mapasGuardados);
  }
});

// Función para regresar a la página anterior
const goBack = () => {
  router.push('/');
};
</script>

<style scoped>
.maps-container {
  padding-top: 100px;
  padding-bottom: 100px;
  min-height: 100vh; /* Cubre toda la pantalla */
  display: flex;
  align-items: center;
  justify-content: center;
}

.text-primary {
  color: #1976d2; /* Color primario de Vuetify */
}

.text-secondary {
  color: #31a31a; /* Color secundario de Vuetify */
}
</style>
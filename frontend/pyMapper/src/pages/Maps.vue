<template>
    <v-container>
      <v-row justify="center">
        <v-col cols="12" md="8">
          <v-card class="pa-6">
            <v-card-title class="text-h4 text-center mb-4">Generated Maps</v-card-title>
            <div v-for="(mapa, index) in mapas" :key="index">
              <v-card class="mb-4">
                <v-card-title>Day {{ index + 1 }}</v-card-title>
                <v-card-text>
                  <!-- Usar v-html para renderizar el HTML crudo del mapa -->
                  <div v-html="mapa"></div>
                </v-card-text>
              </v-card>
            </div>
          </v-card>
        </v-col>
      </v-row>
    </v-container>
  </template>
  
  <script setup>
  import { ref, onMounted } from 'vue';
  
  const mapas = ref([]);
  
  onMounted(() => {
    // Obtener los mapas desde localStorage
    const mapasGuardados = localStorage.getItem('mapas');
    if (mapasGuardados) {
      mapas.value = JSON.parse(mapasGuardados);
    }
  });
  </script>
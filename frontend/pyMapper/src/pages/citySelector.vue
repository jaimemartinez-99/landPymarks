<template>
    <v-container>
      <v-row justify="center">
        <v-col cols="12" md="6">
          <v-card class="pa-6">
            <v-card-title class="text-h4 text-center mb-4">City Selector</v-card-title>
            <v-form @submit.prevent="generateRoute">
              <v-text-field
                v-model="city"
                label="City"
                required
                outlined
                placeholder="Enter a city"
              ></v-text-field>
  
              <v-text-field
                v-model="numberOfDays"
                label="Number of Days"
                type="number"
                required
                outlined
                placeholder="Enter number of days"
              ></v-text-field>
  
            <v-btn type="submit" color="primary" block @click="generateRoute">Generate</v-btn>
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
  const router = useRouter();
  
  const generateRoute = async () => {
    const url = `http://127.0.0.1:8000/generar-ruta/?ciudad=${encodeURIComponent(city.value)}&num_dias=${parseInt(numberOfDays.value)}`;
    try {
        const response = await axios.post(url, null, {
        headers: {
            'Content-Type': 'application/json', // Opcional, dependiendo del backend
        },
        });

        console.log('Response from backend:', response.data); // Verifica la respuesta

        localStorage.setItem('mapas', JSON.stringify(response.data.mapas));

        router.push('/maps');
    } catch (error) {
        console.error('Error generating route:', error);
        alert('Error generating route. Please try again.');
    }
};
  </script>
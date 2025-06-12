<template>
  <v-container
    fluid
    class="city-days-wrapper pa-0 d-flex flex-column align-center justify-center"
  >
    <!-- Título Optimapper -->
    <h1 class="optimapper-title mb-10">Optimapper</h1>
    
    <v-card
      class="selector-card px-8 py-10"
      elevation="6"
      max-width="440"
      outlined
    >
      <v-card-title class="selector-title">
        Plan Your Trip
      </v-card-title>

      <v-card-text>
        <!-- Input ciudad (libre) -->
        <v-text-field
          v-model="city"
          label="Enter city"
          outlined
          dense
          clearable
          placeholder="e.g., Córdoba"
          class="mb-6"
        />

        <!-- Input días -->
        <v-text-field
          v-model.number="days"
          label="Number of days"
          type="number"
          min="1"
          outlined
          dense
          clearable
          class="mb-6"
          @keypress="onlyNumbers"
        />
      </v-card-text>

      <v-card-actions class="justify-center">
        <v-btn
          color="primary"
          :disabled="!isValid || loading"
          @click="goToPlanner"
          large
          class="select-btn"
        >
          <template v-if="loading">
            <v-progress-circular
              indeterminate
              size="24"
              width="3"
              color="#1e3a8a" 
            ></v-progress-circular>
          </template>
          <template v-else>
            Start Planning
          </template>
        </v-btn>
      </v-card-actions>
    </v-card>
  </v-container>
</template>

<script setup>
import { ref, computed } from 'vue';
import { useRouter } from 'vue-router';
import axios from 'axios';

const city = ref('');
const days = ref(0);
const loading = ref(false);
const router = useRouter();

const isValid = computed(() => {
  return city.value.trim() !== '' && days.value > 0;
});

// Función para permitir solo números en input días
const onlyNumbers = (e) => {
  const char = String.fromCharCode(e.keyCode);
  if (!/[0-9]/.test(char)) {
    e.preventDefault();
  }
};

const generateRoute = async () => {
  loading.value = true;
  const url = `https://landpymarks.onrender.com/generate-route/?city=${encodeURIComponent(city.value)}&num_days=${parseInt(days.value)}`;

  try {
    const response = await axios.post(url, null, {
      headers: {
        'Content-Type': 'application/json',
      },
    });

    const uuid = response.data.link;

    localStorage.setItem(response.data.link, JSON.stringify(response.data.maps));
    localStorage.setItem('ciudad', city.value);
    localStorage.setItem('num_dias', days.value);

    router.push({ path: `/${uuid}` });
  } catch (error) {
    console.error('Error generating route:', error);
    alert('Error generating route. Please try again.');
  } finally {
    loading.value = false;
  }
};

const goToPlanner = () => {
  if (!isValid.value) return;
  generateRoute();
};
</script>

<style scoped>
.city-days-wrapper {
  min-height: 100vh;
  background-color: #e0f2fe;
  font-family: "Inter", sans-serif;
  padding-top: 2rem;
}

.optimapper-title {
  font-family: "Inter", sans-serif;
  font-weight: 800;
  font-size: 3rem;
  color: #1e3a8a;
  text-align: center;
  text-shadow: 0 2px 4px rgba(30, 58, 138, 0.2);
  margin-bottom: 1.5rem;
}

.selector-card {
  background-color: #ffffff;
  border-radius: 16px;
  color: #1e3a8a;
  width: 100%;
  max-width: 440px;
  box-shadow: 0 8px 24px rgba(59, 130, 246, 0.15);
}

.selector-title {
  font-weight: 700;
  font-size: 2rem;
  color: #1e3a8a;
  text-align: center;
  margin-bottom: 2rem;
}

.select-btn {
  background-color: #3b82f6;
  color: white !important;
  font-weight: 600;
  width: 100%;
  transition: all 0.2s ease;
}

.select-btn:disabled {
  background-color: #93c5fd;
  cursor: not-allowed;
}

.select-btn:hover:not(:disabled) {
  background-color: #2563eb;
  transform: translateY(-2px);
}
</style>
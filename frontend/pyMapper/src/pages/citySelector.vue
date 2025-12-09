<template>
  <v-container
    fluid
    class="fill-height bg-background d-flex flex-column align-center justify-center position-relative overflow-hidden"
  >
    <!-- Decorative background element -->
    <div class="blob-bg-2" />

    <v-fade-transition appear>
      <div class="d-flex flex-column align-center z-index-1 w-100 px-4">
        <!-- Título Optimapper -->
        <h1
          class="text-h3 text-md-h2 font-weight-black text-primary mb-10 text-center"
          style="line-height: 1.2;"
        >
          Optimapper
        </h1>
        
        <v-card
          class="px-6 py-8 px-md-10 py-md-12 rounded-xl"
          elevation="6"
          width="100%"
          max-width="480"
          border
        >
          <div class="text-center mb-8">
            <h2 class="text-h4 font-weight-bold text-high-emphasis">
              Plan Your Trip
            </h2>
            <p class="text-body-2 text-medium-emphasis mt-2">
              Enter your destination and available time
            </p>
          </div>

          <v-card-text class="pa-0">
            <!-- Input ciudad (libre) -->
            <v-text-field
              v-model="city"
              label="Where to?"
              variant="outlined"
              color="primary"
              bg-color="surface"
              placeholder="e.g., Córdoba, Spain"
              prepend-inner-icon="mdi-map-marker"
              class="mb-4"
            />

            <!-- Input días -->
            <v-text-field
              v-model.number="days"
              label="How many days?"
              type="number"
              min="1"
              variant="outlined"
              color="primary"
              bg-color="surface"
              prepend-inner-icon="mdi-calendar"
              class="mb-6"
              @keypress="onlyNumbers"
            />
          </v-card-text>

          <v-card-actions class="pa-0">
            <v-btn
              color="primary"
              block
              size="x-large"
              :disabled="!isValid || loading"
              :loading="loading"
              class="font-weight-bold"
              elevation="2"
              @click="goToPlanner"
            >
              Generate Itinerary
            </v-btn>
          </v-card-actions>
        </v-card>
      </div>
    </v-fade-transition>
  </v-container>
</template>

<script setup>
import { ref, computed } from 'vue';
import { useRouter } from 'vue-router';
import axios from 'axios';

const city = ref('');
const days = ref(null); // Changed to null so it's empty initially
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
  // Note: hardcoded localhost URL. In a real app this should be an env variable.
  const url = `http://127.0.0.1:8000/generate-route/?city=${encodeURIComponent(city.value)}&num_days=${parseInt(days.value)}`;

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
.z-index-1 {
  z-index: 1;
}

.blob-bg-2 {
  position: absolute;
  bottom: -20%;
  right: -10%;
  width: 60%;
  height: 60%;
  background: radial-gradient(circle, rgba(var(--v-theme-secondary), 0.1) 0%, rgba(0,0,0,0) 70%);
  filter: blur(80px);
  z-index: 0;
  border-radius: 50%;
}
</style>
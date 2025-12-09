<template>
  <v-container
    fluid
    class="fill-height pa-0 d-flex flex-column align-center justify-center position-relative overflow-hidden animated-gradient-bg"
  >
    <div class="overlay-pattern"></div>

    <v-fade-transition appear>
      <div class="d-flex flex-column align-center z-index-1 w-100 px-4">
        
        <v-card
          class="glass-card px-8 py-10 rounded-xl"
          elevation="10"
          width="100%"
          max-width="500"
        >
          <div class="text-center mb-8">
            <h1 class="text-h3 font-weight-black mb-2 text-primary">
              Optimapper
            </h1>
            <p class="text-subtitle-1 text-medium-emphasis">
              Design Your Perfect Journey
            </p>
          </div>

          <v-card-text class="pa-0 mt-6">
            <v-label class="mb-2 font-weight-bold ml-1 text-caption text-uppercase text-medium-emphasis">Destination</v-label>
            <v-text-field
              v-model="city"
              placeholder="e.g., Paris, Tokyo, New York"
              variant="outlined"
              color="primary"
              bg-color="background"
              density="comfortable"
              prepend-inner-icon="mdi-map-marker-radius-outline"
              class="mb-4 rounded-lg"
              hide-details="auto"
            ></v-text-field>

            <v-label class="mb-2 font-weight-bold ml-1 text-caption text-uppercase text-medium-emphasis">Duration</v-label>
            <v-text-field
              v-model.number="days"
              placeholder="Number of days"
              type="number"
              min="1"
              variant="outlined"
              color="primary"
              bg-color="background"
              density="comfortable"
              prepend-inner-icon="mdi-calendar-clock-outline"
              class="mb-8 rounded-lg"
              hide-details="auto"
              @keypress="onlyNumbers"
            ></v-text-field>
          </v-card-text>

          <v-card-actions class="pa-0">
            <v-btn
              color="background"
              block
              size="x-large"
              height="56"
              :disabled="!isValid || loading"
              :loading="loading"
              class="text-body-1 font-weight-bold rounded-lg gradient-btn text-white"
              elevation="4"
              @click="goToPlanner"
            >
              Start Adventure
              <v-icon end icon="mdi-arrow-right" class="ml-2"></v-icon>
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
const days = ref(null);
const loading = ref(false);
const router = useRouter();

const isValid = computed(() => {
  return city.value.trim() !== '' && days.value > 0;
});

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
.animated-gradient-bg {
  background: linear-gradient(-45deg, #f8fafc, #e2e8f0, #bfdbfe, #e0f2fe);
  background-size: 400% 400%;
  animation: gradient 20s ease infinite;
}

@keyframes gradient {
  0% {
    background-position: 0% 50%;
  }
  50% {
    background-position: 100% 50%;
  }
  100% {
    background-position: 0% 50%;
  }
}

.overlay-pattern {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-image: radial-gradient(rgba(255, 255, 255, 0.1) 1px, transparent 1px);
  background-size: 20px 20px;
  pointer-events: none;
}

.z-index-1 {
  z-index: 1;
}

.glass-card {
  background: rgba(255, 255, 255, 0.9) !important;
  backdrop-filter: blur(20px);
  border: 1px solid rgba(255, 255, 255, 0.8);
  box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.37) !important;
}

.gradient-btn {
  background: linear-gradient(90deg, #2563EB 0%, #3B82F6 100%) !important;
  color: white !important;
  transition: transform 0.2s ease, box-shadow 0.2s ease;
}

.gradient-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 10px 20px -5px rgba(37, 99, 235, 0.5);
}
</style>
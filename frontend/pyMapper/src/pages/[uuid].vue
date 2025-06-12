<template>
  <v-container class="maps-container">
    <v-row justify="center">
      <v-col cols="12" lg="10" xl="8">
        <div class="header-wrapper mb-6 text-center">
          <h1 class="optimapper-title mb-1">Optimapper</h1>
          <v-card-title class="trip-title text-h4 font-weight-bold">
            {{ capitalize(ciudad) }}
            <span class="days-badge ml-3">{{ num_dias }} {{ pluralizeDay(num_dias) }}</span>
          </v-card-title>
        </div>

        <v-card elevation="10" rounded="lg">
          <v-expansion-panels class="day-panels">
            <v-expansion-panel
              v-for="(mapa, index) in mapas"
              :key="index"
            >
              <v-expansion-panel-title class="day-title px-6">
                <template v-slot:default="{ expanded }">
                  <v-row no-gutters align="center">
                    <v-col cols="auto">
                      <v-icon large color="blue" class="mr-3">mdi-calendar</v-icon>
                    </v-col>
                    <v-col>
                      <span class="text-h5 font-weight-bold">Day {{ index + 1 }}</span>
                    </v-col>
                  </v-row>
                </template>
              </v-expansion-panel-title>
              
              <v-expansion-panel-text class="panel-content">
                <v-row no-gutters>
                  <v-col cols="12" md="8" class="map-col">
                    <div class="map-wrapper">
                      <div class="map-content" v-html="mapa"></div>
                    </div>
                  </v-col>
                  
                  <v-col cols="12" md="4" class="places-col">
                    <v-card class="places-card h-120" elevation="0" rounded="0">
                      <v-card-text class="px-4 pb-0">
                        <v-list lines="two" density="comfortable">
                          <v-list-item
                            v-for="(place, pIndex) in extractPlaces(mapa)"
                            :key="pIndex"
                            class="px-0"
                          >
                            <template v-slot:prepend>
                              <v-avatar size="24" color="blue-lighten-5">
                                <span class="text-caption text-blue">{{ pIndex + 1 }}</span>
                              </v-avatar>
                            </template>
                            <v-list-item-title class="font-weight-bold text-caption">{{ place }}</v-list-item-title>
                          </v-list-item>
                        </v-list>
                      </v-card-text>
                      <v-card-actions class="px-4 pb-4">
                        <v-btn
                          color="#1e3a8a"
                          variant="outlined"
                          block
                          @click="copyDay(index)"
                        >
                          <v-icon left>mdi-content-copy</v-icon>
                          Copy Itinerary
                        </v-btn>
                      </v-card-actions>
                    </v-card>
                  </v-col>
                </v-row>
              </v-expansion-panel-text>
            </v-expansion-panel>
          </v-expansion-panels>

          <v-card-actions class="px-6 pb-6 pt-3">
            <v-btn
              color="#e0f2fe"
              size="large"
              block
              @click="goBack"
              class="back-btn"
            >
              <v-icon left>mdi-arrow-left</v-icon>
              Plan Another Trip
            </v-btn>
          </v-card-actions>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { useRouter, useRoute } from 'vue-router';

const mapas = ref([]); 
const ciudad = ref(''); 
let num_dias = 0;
const router = useRouter();
const route = useRoute();

const capitalize = (text) => {
  if (!text) return '';
  return text.charAt(0).toUpperCase() + text.slice(1).toLowerCase();
};

const pluralizeDay = (num) => {
  return num > 1 ? 'days' : 'day';
};

const extractPlaces = (htmlContent) => {
  try {
    const unescapeHtml = (text) => {
      return text
        .replace(/&lt;/g, '<')
        .replace(/&gt;/g, '>')
        .replace(/&quot;/g, '"')
        .replace(/&#39;/g, "'")
        .replace(/&amp;/g, '&');
    };

    const cleanContent = unescapeHtml(htmlContent);

    const pointMatches = Array.from(cleanContent.matchAll(/Point \d+:\s*([^<]+)/g))
      .map(match => match[1].trim())
      .filter(name => name.length > 0);

    if (pointMatches.length > 0) return pointMatches;

    const divMatches = Array.from(cleanContent.matchAll(/<div[^>]*>([^<]+)<\/div>/g))
      .map(match => match[1].trim())
      .filter(name =>
        name.length > 0 &&
        !name.startsWith('Point') &&
        !name.match(/html_[\w\d]+/) &&
        !name.match(/width:|height:/)
      );

    if (divMatches.length > 0) return divMatches;

    const textMatches = Array.from(cleanContent.matchAll(/>([^<>]{4,}?)</g))
      .map(match => match[1].trim())
      .filter(name =>
        !name.match(/^(var|html|map|marker|popup|setContent|function|addTo|bindPopup)/) &&
        !name.match(/[{};=]/)
      );

    return textMatches.length > 0 ? textMatches : ['Lugares no identificados'];
  } catch (error) {
    console.error('Error al extraer lugares:', error);
    return ['Failed getting itinerary'];
  }
};

const copyDay = (index) => {
  try {
    const htmlContent = mapas.value[index];
    const places = extractPlaces(htmlContent);

    const formattedText = places.join('\n');

    navigator.clipboard.writeText(formattedText)
      .then(() => {
        alert('Itinerary copied to the clipboard');
      })
      .catch(err => {
        console.error('Failed copying itinerary: ', err);
      });
  } catch (error) {
    console.error('Failed copyDay: ', error);
  }
};

onMounted(() => {
  const uuid = route.params.uuid;
  const mapasGuardados = localStorage.getItem(uuid);
  const ciudadGuardada = localStorage.getItem('ciudad');
  const numDiasGuardados = localStorage.getItem('num_dias');
  
  if (mapasGuardados) {
    mapas.value = JSON.parse(mapasGuardados);
    ciudad.value = ciudadGuardada;
    num_dias = numDiasGuardados;
  } else {
    fetch(`https://landpymarks.onrender.com/retrieve_existing_map/${uuid}`)
      .then(response => response.json())
      .then(data => {
        mapas.value = data.maps;
        ciudad.value = data.city; 
        num_dias = data.num_days;
      })
      .catch(error => {
        console.error('Error fetching data:', error);
        router.push('/');
      });
  }
});

const goBack = () => {
  router.push('/');
};
</script>

<style scoped>
.maps-container {
  padding-top: 30px;
  padding-bottom: 60px;
  min-height: 100vh;
  background-color: #e0f2fe;
}

.optimapper-title {
  font-family: "Inter", sans-serif;
  font-weight: 800;
  font-size: 2.2rem;
  color: #1e3a8a;
  text-shadow: 0 2px 4px rgba(30, 58, 138, 0.2);
}

.trip-title {
  color: #1e3a8a;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-wrap: wrap;
  padding: 8px 0 !important;
}

.days-badge {
  background-color: #3b82f6;
  color: white;
  padding: 4px 12px;
  border-radius: 20px;
  font-size: 1.2rem;
}

.header-wrapper {
  margin-bottom: 24px;
}

.day-panels {
  border-radius: 0 !important;
}

.day-title {
  background-color: #c6daed !important;
  min-height: 72px;
}

.panel-content {
  padding: 0 !important;
}

.map-col {
  position: relative;
  border-right: 1px solid #e0e0e0;
}

.map-wrapper {
  position: relative;
  padding-bottom: 56.25%; /* 16:9 Aspect Ratio */
  height: 0;
  overflow: hidden;
}

.map-content {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  border: none;
}

.places-col {
  background-color: #92b5d6;
}

.places-card {
  border-left: none !important;
  background-color: #92b5d6;
}

.back-btn {
  font-weight: 600;
  letter-spacing: 0.5px;
}

/* Responsive adjustments */
@media (max-width: 959px) {
  .map-col {
    border-right: none;
    border-bottom: 1px solid #e0e0e0;
  }
  
  .map-wrapper {
    padding-bottom: 75%; /* Taller aspect ratio for mobile */
  }
}
</style>
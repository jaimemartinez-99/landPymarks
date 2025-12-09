<template>
  <v-container
    fluid
    class="fill-height bg-background pa-0 align-start"
  >
    <div class="w-100 pa-6 pa-md-10">
      <div class="header-wrapper mb-8 text-center">
        <v-btn
          variant="text"
          color="primary"
          class="mb-4"
          prepend-icon="mdi-arrow-left"
          @click="goBack"
        >
          Back to Planner
        </v-btn>

        <h1 class="text-h3 font-weight-black text-primary mb-2">
          {{ capitalize(ciudad) }}
        </h1>
        <v-chip
          color="secondary"
          variant="tonal"
          size="large"
          class="font-weight-bold"
        >
          {{ num_dias }} {{ pluralizeDay(num_dias) }} Trip
        </v-chip>
      </div>

      <v-row justify="center">
        <v-col
          cols="12"
          lg="10"
          xl="8"
        >
          <v-expansion-panels
            variant="popout"
            class="day-panels"
          >
            <v-expansion-panel
              v-for="(mapa, index) in mapas"
              :key="index"
              elevation="2"
              rounded="xl"
            >
              <v-expansion-panel-title class="py-4">
                <template #default="{ expanded }">
                  <v-row
                    no-gutters
                    align="center"
                  >
                    <v-col cols="auto">
                      <v-avatar
                        color="primary"
                        variant="tonal"
                        class="mr-4"
                      >
                        <span class="font-weight-bold">{{ index + 1 }}</span>
                      </v-avatar>
                    </v-col>
                    <v-col>
                      <span class="text-h6 font-weight-bold">Day {{ index + 1 }} Itinerary</span>
                    </v-col>
                  </v-row>
                </template>
              </v-expansion-panel-title>
              
              <v-expansion-panel-text class="pa-0">
                <v-row no-gutters>
                  <!-- MAP COLUMN -->
                  <v-col
                    cols="12"
                    md="8"
                    class="map-col"
                  >
                    <div class="map-wrapper rounded-lg overflow-hidden ma-2 border">
                      <div
                        class="map-content"
                        v-html="mapa"
                      />
                    </div>
                  </v-col>
                  
                  <!-- PLACES LIST COLUMN -->
                  <v-col
                    cols="12"
                    md="4"
                    class="places-col border-s"
                  >
                    <div class="d-flex flex-column h-100">
                      <div class="px-4 py-3 bg-surface-light border-b">
                        <span class="text-subtitle-2 text-medium-emphasis font-weight-bold text-uppercase">Destinations</span>
                      </div>
                      <v-list
                        class="flex-grow-1 overflow-y-auto"
                        style="max-height: 500px;"
                        lines="two"
                      >
                        <v-list-item
                          v-for="(place, pIndex) in extractPlaces(mapa)"
                          :key="pIndex"
                          class="px-4 py-2"
                        >
                          <template #prepend>
                            <v-icon
                              size="small"
                              color="primary"
                              class="mr-3"
                            >
                              mdi-map-marker
                            </v-icon>
                          </template>
                          <v-list-item-title class="text-body-2 font-weight-medium">
                            {{ place }}
                          </v-list-item-title>
                        </v-list-item>
                      </v-list>
                      
                      <div class="pa-4 border-t mt-auto">
                        <v-btn
                          color="primary"
                          variant="tonal"
                          block
                          prepend-icon="mdi-content-copy"
                          @click="copyDay(index)"
                        >
                          Copy Itinerary
                        </v-btn>
                      </div>
                    </div>
                  </v-col>
                </v-row>
              </v-expansion-panel-text>
            </v-expansion-panel>
          </v-expansion-panels>

          <div class="d-flex justify-center mt-12 pb-10">
            <v-btn
              color="primary"
              size="x-large"
              variant="flat"
              width="280"
              prepend-icon="mdi-plus"
              class="font-weight-bold"
              @click="goBack"
            >
              Plan Another Trip
            </v-btn>
          </div>
        </v-col>
      </v-row>
    </div>
  </v-container>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { useRouter, useRoute } from 'vue-router';

const mapas = ref([]); 
const ciudad = ref(''); 
const num_dias = ref(0); // Made reactive
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

    // Regex adjustments to match typical leaflet output or markers
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
    // Note: hardcoded localhost URL.
    fetch(`http://127.0.0.1:8000/retrieve_existing_map/${uuid}`)
      .then(response => response.json())
      .then(data => {
        mapas.value = data.maps;
        ciudad.value = data.city; 
        num_dias.value = data.num_days; // Update reactive ref
      })
      .catch(error => {
        console.error('Error fetching data:', error);
        // In dev, we might stay here or redirect. Redirecting is safer.
        router.push('/');
      });
  }
);

const goBack = () => {
  router.push('/');
};
</script>

<style scoped>
.map-wrapper {
  position: relative;
  padding-bottom: 56.25%; /* 16:9 Aspect Ratio */
  height: 0;
  overflow: hidden;
  background-color: #f0f0f0;
}

.map-content {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  border: none;
}

/* Responsive adjustments */
@media (max-width: 959px) {
  .map-wrapper {
    padding-bottom: 75%; /* Taller aspect ratio for mobile */
  }
}
</style>
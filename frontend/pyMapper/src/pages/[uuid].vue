<template>
  <v-container class="maps-container">
    <v-row justify="center">
      <v-col cols="12" md="8">
        <v-card class="pa-6" elevation="10">
          <v-card-title class="text-h3 font-weight-bold text-center mb-6 text-primary">
            {{ capitalize(ciudad) }}
            -
            {{ num_dias }} {{ capitalize(pluralizeDay(num_dias))}}
          </v-card-title>

          <div v-for="(mapa, index) in mapas" :key="index" class="mb-6">
            <v-card>
              <v-card-title class="text-h5 font-weight-bold">
                Day {{ index + 1 }}
              </v-card-title>
              <v-card-text>
                <div v-html="mapa"></div> 
              </v-card-text>
            </v-card>
          </div>

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
import { useRouter, useRoute  } from 'vue-router';

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

onMounted(() => {
  const uuid = route.params.uuid;
  const mapasGuardados = localStorage.getItem(uuid);
  const ciudadGuardada = localStorage.getItem('ciudad');
  const numDiasGuardados = localStorage.getItem('num_dias');
  console.log(uuid);
  if (mapasGuardados) {
    mapas.value = JSON.parse(mapasGuardados);
    ciudad.value = ciudadGuardada;
    num_dias = numDiasGuardados;
  } else {
    fetch(`http://127.0.0.1:8000/recuperar_mapa_existente/${uuid}`)
      .then(response => response.json())
      .then(data => {
        mapas.value = data.mapas;
        ciudad.value = data.ciudad; 
        num_dias = data.num_dias;
        console.log
      })
      .catch(error => {
        console.error('Error fetching data:', error);
      });
  }
});

const goBack = () => {
  router.push('/');
};
</script>

<style scoped>
.maps-container {
  padding-top: 100px;
  padding-bottom: 100px;
  min-height: 100vh; 
  display: flex;
  align-items: center;
  justify-content: center;
}

.text-primary {
  color: #1976d2;
  text-transform: capitalize; 
}

.text-secondary {
  color: #f8f8f8; 
  font-size: 10px;
  
}
</style>
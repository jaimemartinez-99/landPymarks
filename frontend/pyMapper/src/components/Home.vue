<template>
  <v-container
    fluid
    class="pa-0 fill-height bg-background"
  >
    <v-row
      no-gutters
      class="fill-height"
    >
      <!-- LEFT SIDE: Hero Content -->
      <v-col
        cols="12"
        md="7"
        lg="8"
        class="d-flex flex-column justify-center align-start px-8 px-md-16 py-12 position-relative overflow-hidden"
      >
        <!-- Background decorative blob (optional) -->
        <div class="blob-bg" />

        <div
          class="z-index-1"
          style="max-width: 800px; width: 100%;"
        >
          <v-chip
            color="primary"
            variant="tonal"
            class="mb-6 font-weight-bold"
            size="small"
          >
            New: Smart Itineraries
          </v-chip>

          <h1
            class="text-h2 text-md-h1 font-weight-black text-primary mb-6"
            style="line-height: 1.1;"
          >
            Smart City Routes<br>
            <span class="text-secondary">for Modern Travelers</span>
          </h1>
          
          <p
            class="text-body-1 text-md-h5 text-medium-emphasis mb-8"
            style="max-width: 600px; line-height: 1.6;"
          >
            Discover top landmarks with optimized, time-saving routes tailored
            to your trip duration. Experience the city like never before.
          </p>
          
          <div class="d-flex gap-4 align-center">
            <v-btn
              color="primary"
              size="x-large"
              height="56"
              elevation="4"
              prepend-icon="mdi-map-search"
              class="px-8"
              @click="goToCitySelector"
            >
              Start Planning
            </v-btn>
            
            <div class="d-flex ml-6">
              <v-btn
                icon="mdi-github"
                variant="text"
                color="medium-emphasis"
                class="mr-2"
                @click="handleClickGithub"
              />
              <v-btn
                icon="mdi-linkedin"
                variant="text"
                color="medium-emphasis"
                @click="handleClickLinkedin"
              />
            </div>
          </div>
        </div>
      </v-col>

      <!-- RIGHT SIDE: Features & Visuals -->
      <v-col
        cols="12"
        md="5"
        lg="4"
        class="bg-surface d-flex flex-column justify-center align-center px-6 py-12 border-s"
      >
        <v-slide-y-transition group>
          <div
            key="feature-1"
            class="feature-card text-center mb-10 w-100"
            style="max-width: 320px"
          >
            <v-avatar
              color="primary"
              variant="tonal"
              size="80"
              class="mb-6 rounded-xl"
            >
              <v-icon
                size="40"
                color="primary"
              >
                mdi-map-marker-path
              </v-icon>
            </v-avatar>
            <h3 class="text-h5 font-weight-bold text-high-emphasis mb-3">
              Optimize Your Journey
            </h3>
            <p class="text-body-2 text-medium-emphasis px-4">
              Our route optimizer calculates the best path between must-see attractions.
            </p>
          </div>

          <div
            key="feature-2"
            class="feature-card text-center mb-10 w-100"
            style="max-width: 320px"
          >
            <v-avatar
              color="secondary"
              variant="tonal"
              size="80"
              class="mb-6 rounded-xl"
            >
              <v-icon
                size="40"
                color="secondary"
              >
                mdi-clock-fast
              </v-icon>
            </v-avatar>
            <h3 class="text-h5 font-weight-bold text-high-emphasis mb-3">
              Save Time
            </h3>
            <p class="text-body-2 text-medium-emphasis px-4">
              Avoid unnecessary detours. Focus on what matters most: exploring.
            </p>
          </div>

          <div
            key="feature-3"
            class="feature-card text-center w-100"
            style="max-width: 320px"
          >
            <v-avatar
              color="warning"
              variant="tonal"
              size="80"
              class="mb-6 rounded-xl"
            >
              <v-icon
                size="40"
                color="warning"
              >
                mdi-star-outline
              </v-icon>
            </v-avatar>
            <h3 class="text-h5 font-weight-bold text-high-emphasis mb-3">
              Top Picks
            </h3>
            <p class="text-body-2 text-medium-emphasis px-4">
              Receive the most popular and culturally relevant recommendations.
            </p>
          </div>
        </v-slide-y-transition>
      </v-col>
    </v-row>
  </v-container>
</template>

<script setup>
import { useRouter } from "vue-router";

const router = useRouter();

const handleClickGithub = () => {
  window.open("https://github.com/jaimemartinez-99/", "_blank");
};

const handleClickLinkedin = () => {
  window.open(
    "https://www.linkedin.com/in/jaime-martínez-ramón-4588522a6",
    "_blank"
  );
};

const goToCitySelector = () => {
  router.push("/cityselector");
};
</script>

<style scoped>
.z-index-1 {
  z-index: 1;
}

.blob-bg {
  position: absolute;
  top: -20%;
  left: -10%;
  width: 50%;
  height: 50%;
  background: radial-gradient(circle, rgba(var(--v-theme-primary), 0.1) 0%, rgba(0,0,0,0) 70%);
  filter: blur(60px);
  z-index: 0;
  border-radius: 50%;
}
</style>

<template>
  <v-container fluid class="landing-wrapper pa-0">
    <v-row no-gutters class="split-hero">
      <!-- IZQUIERDA 70% -->
      <v-col
        cols="12"
        md="8"
        class="hero-left d-flex flex-column justify-center px-10 py-12"
      >
        <div>
          <h1 class="hero-title">
            Smart City Routes<br />
            for Modern Travelers
          </h1>
          <p class="hero-subtitle mt-4">
            Discover top landmarks with optimized, time-saving routes tailored
            to your trip duration.
          </p>
          <v-btn
            class="start-btn mt-6"
            color="primary"
            size="large"
            @click="goToCitySelector"
          >
            Start Planning
          </v-btn>
        </div>
      </v-col>

      <!-- DERECHA 30% -->
      <v-col
        cols="12"
        md="4"
        class="hero-right d-flex flex-column justify-center align-center px-6 py-12"
      >
        <v-icon size="64" color="#3b82f6" class="mb-4"
          >mdi-map-marker-path</v-icon
        >
        <h2 class="text-h6 font-weight-bold mb-2" style="color: #334155">
          Optimize Your Journey
        </h2>
        <p
          class="text-body-2 text-muted text-center mb-6"
          style="max-width: 280px"
        >
          Our route optimizer calculates the best path between must-see
          attractions in your selected city
        </p>

        <v-icon size="48" color="#3b82f6" class="mb-2"
          >mdi-clock-outline</v-icon
        >
        <h2 class="text-h6 font-weight-bold mb-2" style="color: #334155">
          Save Time
        </h2>
        <p
          class="text-body-2 text-muted text-center mb-6"
          style="max-width: 240px"
        >
          Avoid unnecessary detours. Focus on what matters most: exploring
        </p>

        <v-icon size="48" color="#3b82f6" class="mb-2">mdi-star-outline</v-icon>
        <h2 class="text-h6 font-weight-bold mb-2" style="color: #334155">
          Top Picks
        </h2>
        <p class="text-body-2 text-muted text-center" style="max-width: 240px">
          You will receive the most popular and culturally relevant recommendations
        </p>
        <div class="flex mt-6">
          <!-- Botón GitHub -->
          <button
            class="bg-white hover:bg-blue-100 text-blue-500 p-3 mr-3 rounded-full transition-shadow shadow-sm hover:shadow-md"
            @click="handleClickGithub"
            aria-label="GitHub"
          >
            <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="#3b82f6">
              <path
                d="M12 0c-6.626 0-12 5.373-12 12 
                  0 5.302 3.438 9.8 8.207 11.387.599.111.793-.261.793-.577v-2.234c-3.338.726-4.033-1.416-4.033-1.416
                  -.546-1.387-1.333-1.756-1.333-1.756-1.089-.745.083-.729.083-.729 
                  1.205.084 1.839 1.237 1.839 1.237 1.07 1.834 2.807 1.304 3.492.997.107-.775.418-1.305.762-1.604
                  -2.665-.305-5.467-1.334-5.467-5.931 0-1.311.469-2.381 1.236-3.221
                  -.124-.303-.535-1.524.117-3.176 0 0 1.008-.322 3.301 1.23
                  .957-.266 1.983-.399 3.003-.404 1.02.005 2.047.138 3.006.404 
                  2.291-1.552 3.297-1.23 3.297-1.23.653 1.653.242 2.874.118 3.176
                  .77.84 1.235 1.911 1.235 3.221 0 4.609-2.807 5.624-5.479 5.921
                  .43.372.823 1.102.823 2.222v3.293c0 .319.192.694.801.576 
                  4.765-1.589 8.199-6.086 8.199-11.386 0-6.627-5.373-12-12-12z"
              />
            </svg>
          </button>

          <!-- Botón LinkedIn -->
          <button
            class="bg-white hover:bg-blue-100 text-blue-500 p-3 rounded-full transition-shadow shadow-sm hover:shadow-md"
            @click="handleClickLinkedin"
            aria-label="LinkedIn"
          >
            <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="#3b82f6">
              <path
                d="M19 0h-14c-2.761 0-5 2.239-5 5v14c0 
                  2.761 2.239 5 5 5h14c2.762 0 5-2.239 5-5v-14c0-2.761-2.238-5-5-5zm-11 
                  19h-3v-11h3v11zm-1.5-12.268c-.966 0-1.75-.79-1.75-1.764s.784-1.764 
                  1.75-1.764 1.75.79 1.75 1.764-.783 1.764-1.75 
                  1.764zm13.5 12.268h-3v-5.604c0-3.368-4-3.113-4 
                  0v5.604h-3v-11h3v1.765c1.396-2.586 7-2.777 
                  7 2.476v6.759z"
              />
            </svg>
          </button>
        </div>
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
.landing-wrapper {
  background-color: #f1f5f9;
  min-height: 100vh;
  font-family: "Inter", sans-serif;
}

.split-hero {
  min-height: 100vh;
}

.hero-left {
  background-color: #e0f2fe;
  color: #1e3a8a;
}

.hero-title {
  font-size: 5rem;
  font-weight: 800;
  line-height: 1.2;
  color: #1e3a8a;
}

.hero-subtitle {
  font-size: 1.2rem;
  color: #475569;
  max-width: 600px;
}

.start-btn {
  font-weight: 600;
  font-size: 1rem;
  padding: 14px 32px;
  background-color: #3b82f6;
  color: white;
  box-shadow: 0 4px 14px rgba(59, 130, 246, 0.3);
  transition: all 0.2s ease;
}

.start-btn:hover {
  background-color: #2563eb;
  transform: translateY(-2px);
}

.hero-right {
  background-color: #f8fafc;
  color: #1f2937;
  text-align: center;
}

.text-muted {
  color: #64748b;
}
</style>

<template>
    <v-container class="home-container">
      <!-- Hero Section -->
      <v-row justify="center" align="center" class="hero-section">
        <v-col cols="12" md="8" class="text-center">
          <h1 class="text-h2 font-weight-bold mb-4">Welcome to Tourist Route Optimizer</h1>
          <p class="text-h6 mb-6">
            Plan your perfect trip with optimized routes tailored to your preferences.
            Explore the best attractions and save time with our intelligent route planner.
          </p>
          <v-btn color="primary" size="large" @click="goToCitySelector">
            Start Planning Now
          </v-btn>
        </v-col>
      </v-row>
  
      <!-- Features Section -->
      <v-row justify="center" class="features-section mt-9">
        <v-col cols="12" class="text-center">
          <h2 class="text-h4 font-weight-bold mb-6">Why Choose Us?</h2>
        </v-col>
        <v-col cols="12" md="4" class="text-center">
          <v-icon size="64" color="primary">mdi-map-marker-path</v-icon>
          <h3 class="text-h5 font-weight-bold mt-4">Optimized Routes</h3>
          <p class="text-body-1">
            We create the most efficient routes to save you time and energy.
          </p>
        </v-col>
        <v-col cols="12" md="4" class="text-center">
          <v-icon size="64" color="primary">mdi-star</v-icon>
          <h3 class="text-h5 font-weight-bold mt-4">Top Attractions</h3>
          <p class="text-body-1">
            Discover the best attractions based on your interests.
          </p>
        </v-col>
        <v-col cols="12" md="4" class="text-center">
          <v-icon size="64" color="primary">mdi-calendar</v-icon>
          <h3 class="text-h5 font-weight-bold mt-4">Flexible Planning</h3>
          <p class="text-body-1">
            Plan your trip for any number of days and customize your experience.
          </p>
        </v-col>
      </v-row>
    </v-container>
  </template>
  
  <script setup>
  import { useRouter } from 'vue-router';
  
  const router = useRouter();
  
  const goToCitySelector = () => {
    router.push('/cityselector');
  };
  </script>
  
  <style scoped>
  .home-container {
    padding-top: 100px;
    padding-bottom: 100px;
  }
  
  .hero-section {
    background: linear-gradient(135deg, #6a11cb, #2575fc);
    padding: 100px 20px;
    border-radius: 16px;
    color: rgb(255, 255, 255);
  }
  
  .features-section {
    padding: 60px 20px;
  }
  
  .cta-section {
    padding: 60px 20px;
  }
  </style>
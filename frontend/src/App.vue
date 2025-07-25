<script setup>
import { RouterLink, RouterView } from 'vue-router';

import { useAuthStore } from '@/stores';

const authStore = useAuthStore();

function logout() {
  console.log("Logging out...");
  // Perform any necessary cleanup or state reset here
  // For example, you might want to clear user data or reset application state
  authStore.logout();
}
</script>

<template>
  <div id="navbar">
      <b-navbar toggleable="lg">
        <b-navbar-brand variant="primary" to="/">Kayak Info</b-navbar-brand>
        <b-navbar-toggle target="nav-collapse"></b-navbar-toggle>
        <b-collapse id="nav-collapse" is-nav>
          <b-navbar-nav>
            <b-nav-item variant="primary" :to="{name: 'LaunchList'}">Boat Launches</b-nav-item>
            <b-nav-item variant="primary" :to="{name: 'WaterList'}">Bodies of Water</b-nav-item>
            <b-nav-item variant="primary" :to="{name: 'TripList'}">Trips</b-nav-item>
            <b-nav-item variant="primary" v-if="!authStore.accesstoken" :to="{name: 'Login'}">Login</b-nav-item>
            <b-nav-item variant="primary" v-else @click="authStore.logout()">Logout</b-nav-item>
          </b-navbar-nav>
        </b-collapse>
      </b-navbar>
  </div>
  <div id="app">
  <router-view />
  </div>
</template>

<style scoped>
header {
  line-height: 1.5;
}

.logo {
  display: block;
  margin: 0 auto 2rem;
}

@media (min-width: 1024px) {
  header {
    display: flex;
    place-items: center;
    padding-right: calc(var(--section-gap) / 2);
  }

}
</style>

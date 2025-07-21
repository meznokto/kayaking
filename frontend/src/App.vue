<script setup>
import { RouterLink, RouterView } from 'vue-router';

import { useAuthStore } from '@/stores';

const authStore = useAuthStore();
</script>

<template>
  <div id="navbar">
      <b-navbar toggleable="lg">
        <b-navbar-brand to="/">Kayak Info</b-navbar-brand>
        <b-navbar-toggle target="nav-collapse"></b-navbar-toggle>
        <b-collapse id="nav-collapse" is-nav>
          <b-navbar-nav>
            <b-nav-item :to="{name: 'LaunchList'}">Boat Launches</b-nav-item>
            <b-nav-item :to="{name: 'WaterList'}">Bodies of Water</b-nav-item>
            <b-nav-item :to="{name: 'TripList'}">Trips</b-nav-item>
            <b-nav-item :to="{name: 'Login'}">Login</b-nav-item>
          </b-navbar-nav>
        </b-collapse>
      </b-navbar>
      <nav v-show="authStore.user" class="navbar navbar-expand navbar-dark bg-dark px-3">
            <div class="navbar-nav">
                <button @click="authStore.logout()" class="btn btn-link nav-item nav-link">Logout</button>
            </div>
        </nav>
    <component :is="currentView"></component>
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

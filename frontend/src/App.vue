<script setup>
import { ref, computed } from 'vue'
import HomePage from './components/HomePage.vue'
import launchInfo from './components/LaunchInfo.vue'

const routes = {
  '/': HomePage,
  '/launchlist': launchInfo,
}

const currentPath = ref(window.location.hash)

window.addEventListener('hashchange', () => {
  currentPath.value = window.location.hash
})

const currentView = computed(() => {
  return routes[currentPath.value.slice(1) || '/'] || NotFound
})
</script>

<template>
  <div id="app">
    <div>
      <b-navbar toggleable="lg" type="dark" variant="info">
        <b-navbar-brand href="#/">Kayak Info</b-navbar-brand>
        <b-navbar-toggle target="nav-collapse"></b-navbar-toggle>
        <b-collapse id="nav-collapse" is-nav>>
          <b-navbar-nav>
          <b-nav-item href="#/">Home</b-nav-item>
          <b-nav-item href="#/launchlist">Launch List</b-nav-item>
          <b-nav-item href="#/waterlist">Water List</b-nav-item>
          <b-nav-item href="#/triplist">Trip List</b-nav-item>
        </b-navbar-nav>
        </b-collapse>
      </b-navbar>
    </div>
    <component :is="currentView"></component>
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

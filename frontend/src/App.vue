<script setup>
</script>

<template>
  <div id="navbar">
      <b-navbar toggleable="lg">
        <b-navbar-brand to="/">Kayak Info</b-navbar-brand>
        <b-navbar-toggle target="nav-collapse"></b-navbar-toggle>
        <b-collapse id="nav-collapse" is-nav>
          <b-navbar-nav>
            <b-nav-item :to="'LaunchList'">Boat Launches</b-nav-item>
            <b-nav-item :to="'WaterList'">Bodies of Water</b-nav-item>
            <b-nav-item :to="'TripList'">Trips</b-nav-item>
          </b-navbar-nav>
        </b-collapse>
      </b-navbar>
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

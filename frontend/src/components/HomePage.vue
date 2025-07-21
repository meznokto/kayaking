<template>
  <div class="app">
    <h1>Kayak Info</h1>
        <h1>Hi!</h1>
        <p>You're logged in with Vue 3 + JWT with Refresh Tokens!!</p>
        <h3>Users from secure api end point:</h3>
        <ul v-if="users.length">
            <li v-for="user in users" :key="user.id">{{user.email}}</li>
        </ul>
        <div v-if="users.loading" class="spinner-border spinner-border-sm"></div>
        <div v-if="users.error" class="text-danger">Error loading users: {{users.error}}</div>
  </div>
</template>

<script setup>
import { storeToRefs } from 'pinia';

import { useAuthStore, useUsersStore } from '@/stores';

const authStore = useAuthStore();
const { user: authUser } = storeToRefs(authStore);

const usersStore = useUsersStore();
const { users } = storeToRefs(usersStore);

usersStore.getAll();
</script>

<style>
.homepage {
  font-family: Arial, sans-serif;
  text-align: center;
  margin-top: 50px;
}

h1 {
  color: #333;
}

button {
  padding: 10px 20px;
  background-color: #42b983;
  color: white;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  margin-top: 20px;
}
</style>
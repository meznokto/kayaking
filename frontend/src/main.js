import { createBootstrap } from 'bootstrap-vue-next'
import { createApp } from 'vue'
import { createPinia } from 'pinia';
import App from './App.vue'
import router from './routes'
import { useAuthStore } from './stores';

import 'bootstrap/dist/css/bootstrap.css'
import 'bootstrap-vue-next/dist/bootstrap-vue-next.css'

//createApp(App).mount('#app')
const app = createApp(App)
app.use(createPinia());
app.use(router)
app.use(createBootstrap())

// attempt to auto refresh token before startup
try {
    const authStore = useAuthStore();
    await authStore.refreshToken();
} catch {
    // catch error to start app on success or failure
    console.error('Failed to refresh token, starting app without user authentication');
}

app.mount('#app')
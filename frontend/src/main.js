import { createBootstrap } from 'bootstrap-vue-next'

import './assets/main.css'
import 'bootstrap/dist/css/bootstrap.css'
import 'bootstrap-vue-next/dist/bootstrap-vue-next.css'

import { createApp } from 'vue'
import App from './App.vue'

//createApp(App).mount('#app')
const app = createApp(App)
app.use(createBootstrap())
app.mount('#app')
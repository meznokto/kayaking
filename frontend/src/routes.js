import { createRouter, createMemoryHistory } from 'vue-router'

import HomePage from './components/HomePage.vue'
import launchList from './components/LaunchList.vue'
import WaterList from './components/WaterList.vue'
import TripList from './components/TripList.vue'
import LaunchDetail from './components/LaunchDetail.vue'

const routes = [
  { path: '/', name: "Home", component: HomePage },
  { path: '/launchlist', name: "LaunchList", component: launchList },
  { path: '/waterlist', name: "WaterList", component: WaterList },
  { path: '/triplist', name: "TripList", component: TripList },
  { path: '/launchdetail/:launchid', name: "LaunchDetail", component: LaunchDetail },
]
const router = createRouter({
  history: createMemoryHistory(),
  routes,
})

export default router
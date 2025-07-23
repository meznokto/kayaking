import { createRouter, createMemoryHistory } from 'vue-router'

import HomePage from './components/HomePage.vue'
import launchList from './components/LaunchList.vue'
import WaterList from './components/WaterList.vue'
import TripList from './components/TripList.vue'
import LaunchDetail from './components/LaunchDetail.vue'
import TripDetail from './components/TripDetail.vue'
import WaterDetail from './components/WaterDetail.vue'
import Login from './components/Login.vue'

const routes = [
  { path: '/', name: "Home", component: HomePage },
  { path: '/login', name: "Login", component: Login },
  { path: '/launchlist', name: "LaunchList", component: launchList },
  { path: '/launchlist/bycity/:city', name: "LaunchListCity", component: launchList },
  { path: '/launchlist/bystate/:state', name: "LaunchListState", component: launchList },
  { path: '/launchlist/bycountry/:country', name: "LaunchListCountry", component: launchList },
  { path: '/launchlist/bycounty/:county', name: "LaunchListCounty", component: launchList },
  { path: '/waterlist', name: "WaterList", component: WaterList },
  { path: '/triplist', name: "TripList", component: TripList },
  { path: '/launchdetail/:launchid', name: "LaunchDetail", component: LaunchDetail },
  { path: '/tripdetail/:tripid', name: "TripDetail", component: TripDetail },
  { path: '/waterdetail/:waterid', name: "WaterDetail", component: WaterDetail },
]
const router = createRouter({
  history: createMemoryHistory(),
  routes,
})

export default router

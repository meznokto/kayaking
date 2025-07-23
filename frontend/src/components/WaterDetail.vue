<template>
<div class="app">
    <div v-if="fetchingWater">
        <p>Loading...</p>
    </div>
	<div v-else class="row">
		<div class="col-md-12">
			<h3>Water Info</h3>
		</div>
		<div class="col-md-12">
            {{ myWater.name }}<br>
            {{ myWater.latitude }}, {{ myWater.longitude }}<br>
            <router-link v-if="myWater.city !== null" :to="{name: 'WaterListCity', params: {city: myWater.city.id }}">{{ myWater.city.name }}, </router-link>
            <router-link v-if="myWater.city !== null" :to="{name: 'WaterListState', params: {state: myWater.state.id }}">{{ myWater.state.abbr }}, </router-link> 
            <router-link v-else :to="{name: 'WaterListState', params: {state: myWater.state.id }}">{{ myWater.state.name }}, </router-link>
            <router-link :to="{name: 'WaterListCountry', params: {country: myWater.country.id }}">{{ myWater.country.abbr }}</router-link><br>
            <router-link :to="{name: 'WaterListCounty', params: {county: myWater.county.id }}">{{ myWater.county.name }} County</router-link><br>
            <a :href="'https://maps.google.com/?q=' + myWater.latitude + ',' + myWater.longitude + '&ll=' + myWater.latitude + ',' + myWater.longitude + '&z=14'" target="_blank">View on Google Maps</a><br>
		</div>
	</div>
    <div v-if="launchList.length > 0">
        <h4>Launches on this body of water:</h4>
        <ul>
            <li v-for="launch in launchList" :key="launch.id">
                <router-link :to="{ name: 'LaunchDetail', params: { launchid: launch.id } }">{{ launch.name }}</router-link>
            </li>
        </ul>
    </div>
    <div v-else>
        <p>No launches found for this body of water.</p>
    </div>
    <button @click="goBack" class="btn btn-secondary mt-3">Go Back</button>
</div>
</template>

<script setup lang="ts">
	import { ref, onMounted } from 'vue'
	import axios from 'axios'
    import { useRoute, useRouter } from 'vue-router';
    import GlobalVariables from '../globals.js'

    const goBack = () => {
        router.go(-1)
    }

	interface water {
        id: number;
		name: string;
        water_type_text: string;
        latitude: number;
        longitude: number;
        city: { id: number; name: string };
        state: { id: number; name: string; abbr: string };
        country: { id: number; abbr: string };
        county: { id: number; name: string };
	}

    interface launch {
		id: number;
		name: string;
		city: { name: string };
		state: { abbr: string };
		country: { abbr: string };
		body_of_water: { id: number; name: string };
		thumbnail: string;
	}

	const myWater = ref(<water>{
        id: 0,
        name: '',
        water_type_text: '',
        latitude: 0,
        longitude: 0,
        city: { id: 0, name: '' },
        state: { id: 0, name: '', abbr: '' },
        country: { id: 0, abbr: '' },
        county: { id: 0, name: '' }
    })

    const launchList = ref([] as launch[])
	const fetchingWater = ref(false)
    const route = useRoute()
    const router = useRouter()

	async function fetchWaterDetail() {
        fetchingWater.value = true
        const id = route.params.waterid

        try {
		    const waterInfoResponse = await axios.get<water[]>(GlobalVariables.apiURL + "waterinfo/?water=" + id + "&fields=all")
        
            if (waterInfoResponse.data.length > 0) {
                myWater.value = waterInfoResponse.data[0]
            }
        } catch(error) {
            console.error("Error fetching water details:", error.message)
        }

        // find launches on this body of water
        try {
		    const launchInfoResponse = await axios.get<launch[]>(GlobalVariables.apiURL + "launchinfo/?waterid=" + id)
		    launchList.value = launchInfoResponse.data
        } catch(error) {
            if (error.response && error.response.status === 404) {
                console.error('Server error (404):', error.response.data);
            } else {
                console.error('Unknown error occurred:', error.message)
            }
        }
        fetchingWater.value = false
	}

	onMounted(async () => {
		await fetchWaterDetail()
	})
</script>

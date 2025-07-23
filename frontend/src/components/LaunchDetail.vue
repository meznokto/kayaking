<template>
<div class="app">
    <div v-if="fetchingLaunch">
        <p>Loading...</p>
    </div>
	<div v=else class="row">
		<div class="col-md-12">
			<h3>Boat Launch Info</h3>
		</div>
		<div class="col-md-12">
            {{ myLaunch.name }} on <router-link :to="{name: 'WaterDetail', params: { waterid: myLaunch.body_of_water.id }}">{{ myLaunch.body_of_water.name }}</router-link><br>
	    <router-link :to="{name: 'LaunchListCity', params: {city: myLaunch.city.id }}">{{ myLaunch.city.name }}</router-link>, 
        <router-link :to="{name: 'LaunchListState', params: {state: myLaunch.state.id }}">{{ myLaunch.state.abbr }}</router-link>, 
        <router-link :to="{name: 'LaunchListCountry', params: {country: myLaunch.country.id }}">{{ myLaunch.country.abbr }}</router-link><br>
        <router-link :to="{name: 'LaunchListCounty', params: {county: myLaunch.county.id }}">{{ myLaunch.county.name }} County</router-link><br>
            {{ myLaunch.latitude }}, {{ myLaunch.longitude }}<br>
            <a :href="'https://www.google.com/maps/dir/?api=1&destination=' + myLaunch.latitude + ',' + myLaunch.longitude" target="_blank">Get directions on Google Maps</a><br>
            <div v-if="myLaunch.main_image !== null">
                <a v-bind:href="GlobalVariables.imgURL + myLaunch.main_image.original" target="_blank">
                    <img v-bind:src="GlobalVariables.imgURL + myLaunch.thumbnail" alt="Launch Image" class="img-fluid">
                </a><br>
            </div>
		</div>
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

	interface launch {
		id: number;
		name: string;
		city: { id: number;
			name: string };
        county: { id: number;
            name: string };
		state: { id: number; 
            abbr: string };
		country: { id: number; 
            abbr: string };
        body_of_water: { id: number; name: string };
        latitude: number;
        longitude: number;
        thumbnail: string;
        main_image: { original: string };
	}

	const myLaunch = ref(<launch>{
        id: 0,
        name: '',
        city: { id: 0, name: '' },
        county: { id: 0, name: '' },
        state: { id: 0, abbr: '' },
        country: { id: 0, abbr: '' },
        body_of_water: { id: 0, name: '' },
        latitude: 0,
        longitude: 0,
        thumbnail: '',
        main_image: null
    })
	const fetchingLaunch = ref(false)
    const route = useRoute()
    const router = useRouter()

	async function fetchLaunchDetail() {
        fetchingLaunch.value = true
        const id = route.params.launchid

        try {
		    const launchInfoResponse = await axios.get<launch[]>(GlobalVariables.apiURL + "launchinfo/?launch=" + id + "&fields=all")
        
            myLaunch.value = launchInfoResponse.data[0]
        } catch(error) {
            console.error("Error fetching launch details:", error.message)
        }
        fetchingLaunch.value = false
	}

	onMounted(async () => {
		await fetchLaunchDetail()
	})
</script>

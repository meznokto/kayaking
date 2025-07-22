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
            {{ myLaunch.city.name }}, {{ myLaunch.state.abbr }}, {{ myLaunch.country.abbr }}<br>
            {{ myLaunch.county.name }} County<br>
            {{ myLaunch.latitude }}, {{ myLaunch.longitude }}<br>
            <a :href="'https://www.google.com/maps/dir/?api=1&destination=' + myLaunch.latitude + ',' + myLaunch.longitude" target="_blank">Get directions on Google Maps</a><br>
            <div v-if="myLaunch.main_image !== null">
                <a v-bind:href="GlobalVariables.imgURL + myLaunch.main_image.original">
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
		city: { name: string };
        county: { name: string };
		state: { abbr: string };
		country: { abbr: string };
        body_of_water: { id: number; name: string };
        latitude: number;
        longitude: number;
        thumbnail: string;
        main_image: { original: string };
	}

	const myLaunch = ref(<launch>{
        id: 0,
        name: '',
        city: { name: '' },
        county: { name: '' },
        state: { abbr: '' },
        country: { abbr: '' },
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
		const launchInfoResponse = await axios.get<launch[]>(GlobalVariables.apiURL + "launchinfo/?launch=" + id + "&fields=all")
        
        if (launchInfoResponse.data.length > 0) {
            myLaunch.value = launchInfoResponse.data[0]
        } else {
            console.error('Launch not found')
        }
        fetchingLaunch.value = false
	}

	onMounted(async () => {
		await fetchLaunchDetail()
	})
</script>

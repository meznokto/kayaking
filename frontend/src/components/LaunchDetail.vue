<template>
<div class="app">
	<div class="row">
		<div class="col-md-12">
			<h3>Boat Launch Info</h3>
		</div>
		<div class="col-md-12">
            {{ myLaunch.name }} on <a :href="'#/waterdetail/' + myLaunch.body_of_water.id">{{ myLaunch.body_of_water.name }}</a><br>
            {{ myLaunch.city.name }}, {{ myLaunch.state.abbr }}, {{ myLaunch.country.abbr }}<br>
            {{ myLaunch.county.name }} County<br>
            {{ myLaunch.latitude }}, {{ myLaunch.longitude }}<br>
            <a v-bind:href="'http://localhost:8000' + myLaunch.main_image.original"><img v-bind:src="'http://localhost:8000' + myLaunch.thumbnail" alt="Launch Image" class="img-fluid"></a><br>
		</div>
	</div>
</div>
</template>

<script setup lang="ts">
	import { ref, onMounted } from 'vue'
	import axios from 'axios'

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
        main_image: { original: '' }
    })
	const fetchingLaunch = ref(false)

	async function fetchLaunchDetail() {
        fetchingLaunch.value = true
		const launchInfoResponse = await axios.get<launch[]>("http://localhost:8000/api/launchinfo/?launch=2&fields=all")
        
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

<template>
<div class="app">
	<div class="row">
		<div class="col-md-12">
			<h3>Water Info</h3>
		</div>
		<div class="col-md-12">
            {{ myWater.name }} ({{ myWater.water_type_text }})<br>
            {{ myWater.latitude }}, {{ myWater.longitude }}<br>
            {{ myWater.city.name }}, {{ myWater.state.abbr }}, {{ myWater.country.abbr }} ({{ myWater.county.name }} County)<br>
		</div>
	</div>
    Back to <router-link :to="{name: 'WaterList'}">Water List</router-link>
</div>
</template>

<script setup lang="ts">
	import { ref, onMounted } from 'vue'
	import axios from 'axios'

	interface water {
		name: string;
        water_type_text: string;
        latitude: number;
        longitude: number;
        city: { name: string };
        state: { abbr: string };
        country: { abbr: string };
        county: { name: string };
	}

	const myWater = ref(<water>{
        name: '',
        water_type_text: '',
        latitude: 0,
        longitude: 0,
        city: { name: '' },
        state: { abbr: '' },
        country: { abbr: '' },
        county: { name: '' }
    })
	const fetchingWater = ref(false)

	async function fetchWaterDetail() {
        fetchingWater.value = true
		const waterInfoResponse = await axios.get<water[]>("http://localhost:8000/api/waterinfo/?water=1&fields=all")
        
        if (waterInfoResponse.data.length > 0) {
            myWater.value = waterInfoResponse.data[0]
        } else {
            console.error('Water not found')
        }
        fetchingWater.value = false
	}

	onMounted(async () => {
		await fetchWaterDetail()
	})
</script>

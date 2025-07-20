<template>
<div class="app">
	<div v-if="fetchingTrips">
		<p>Loading...</p>
	</div>
	<div v-else class="row">
		<div class="col-md-12">
			<h3>Trips</h3>
		</div>
		<div class="col-md-12">
			<ul class="list-group">
				<li v-for="trip in tripList" :key=trip.id class="list-group-item">
					<router-link :to="{name: 'TripDetail', params: { tripid: trip.id }}">
					{{trip.body_of_water.name}} - {{trip.start_time}}</router-link>
				</li>
			</ul>
		</div>
	</div>
</div>
</template>

<script setup lang="ts">
	import { ref, onMounted } from 'vue'
	import axios from 'axios'

	interface trip {
		id: number;
		start_time: string;
		body_of_water: { name: string };
	}

	const tripList = ref([] as trip[])
	const fetchingTrips = ref(false)

	async function loadMoreTrips () {
		fetchingTrips.value = true
		const tripInfoResponse = await axios.get<trip[]>('http://localhost:8000/api/tripinfo/')

		tripList.value.push(...(tripInfoResponse.data || []))
		fetchingTrips.value = false
	}

	async function fetchInitialTrips() {
		const tripInfoResponse = await axios.get<trip[]>('http://localhost:8000/api/tripinfo/')
		tripList.value = tripInfoResponse.data
	}

	onMounted(async () => {
		await fetchInitialTrips()
	})
</script>

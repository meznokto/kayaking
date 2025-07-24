<template>
<div class="app">
	<div class="col-md-12">
		<h3>Trips</h3>
	</div>
	<div v-if="fetchingTrips">
		<b-spinner variant="primary" label="Loading"></b-spinner>
	</div>
	<div v-else class="row">
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
	import { fetchWrapper } from '@/helpers';
	import GlobalVariables from '../globals.js'

	interface trip {
		id: number;
		start_time: string;
		body_of_water: { name: string };
	}

	const tripList = ref([] as trip[])
	const fetchingTrips = ref(false)

	async function loadMoreTrips () {
		fetchingTrips.value = true

		try {
			const tripInfoResponse = await fetchWrapper.get<trip[]>(GlobalVariables.apiURL + 'tripinfo/')

			tripList.value.push(...(tripInfoResponse.data || []))
		} catch(error) {
			console.error("Error fetching trips:", error.message)
		}
		fetchingTrips.value = false
	}

	async function fetchInitialTrips() {
		fetchingTrips.value = true

		try {
			const tripInfoResponse = await fetchWrapper.get<trip[]>(GlobalVariables.apiURL + 'tripinfo/')
			tripList.value = tripInfoResponse
		} catch(error) {
			console.error("Error fetching initial trips:", error.message)
		}
		fetchingTrips.value = false
	}

	onMounted(async () => {
		await fetchInitialTrips()
	})
</script>

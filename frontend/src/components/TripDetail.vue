<template>
<div class="app">
	<div class="row">
		<div class="col-md-12">
			<h3>Trip Info</h3>
		</div>
		<div class="col-md-12">
            <a :href="'#/waterdetail/' + myTrip.body_of_water.id">{{ myTrip.body_of_water.name }}</a><br>
            {{ myTrip.start_time }} - {{ myTrip.end_time }}<br>
            From {{ myTrip.start_launch.name }} to {{ myTrip.end_launch.name }}<br>
            {{ myTrip.notes }}
		</div>
	</div>
    Back to <router-link :to="{name: 'TripList'}">Trip List</router-link>
</div>
</template>

<script setup lang="ts">
	import { ref, onMounted } from 'vue'
	import axios from 'axios'

	interface trip {
		id: number;
        start_time: string;
        end_time: string;
        body_of_water: { id: number; name: string };
        start_launch: { name: string };
        end_launch: { name: string };
        notes: string;
	}

	const myTrip = ref(<trip>{
        id: 0,
        start_time: '',
        end_time: '',
        body_of_water: { id: 0, name: '' },
        start_launch: { name: '' },
        end_launch: { name: '' },
        notes: ''
    })
	const fetchingTrip = ref(false)

	async function fetchTripDetail() {
        fetchingTrip.value = true
		const tripInfoResponse = await axios.get<trip[]>("http://localhost:8000/api/tripinfo/?trip=1&fields=all")
        
        if (tripInfoResponse.data.length > 0) {
            myTrip.value = tripInfoResponse.data[0]
        } else {
            console.error('Trip not found')
        }
        fetchingTrip.value = false
	}

	onMounted(async () => {
		await fetchTripDetail()
	})
</script>

<template>
<div class="app">
    <div class="col-md-12">
		<h3>Trip Info</h3>
	</div>
    <div v-if="fetchingTrip">
        <b-spinner variant="primary" label="Loading"></b-spinner>
    </div>
	<div v-else class="row">
		<div class="col-md-12">
            <router-link :to="{name: 'WaterDetail', params: { waterid: myTrip.body_of_water.id }}">{{ myTrip.body_of_water.name }}</router-link><br>
            {{ dayjs(myTrip.start_time).format('MMMM D, YYYY') }}<br>
            Start: {{ myTrip.start_launch.name }} at {{ dayjs(myTrip.start_time).format('h:mm A') }}<br>
            End: {{ myTrip.end_launch.name }} at {{ dayjs(myTrip.end_time).format('h:mm A') }}
            <template v-if="dayjs(myTrip.start_time).format('YYYY-MM-DD') !== dayjs(myTrip.end_time).format('YYYY-MM-DD')">
                ({{ dayjs(myTrip.end_time).format('MMMM D') }})
            </template>
            <br>
            {{ myTrip.notes }}
		</div>
	</div>
    <button @click="goBack" class="btn btn-secondary mt-3">Go Back</button>
</div>
</template>

<script setup lang="ts">
	import { ref, onMounted } from 'vue'
    import { useRoute, useRouter } from 'vue-router';
    import dayjs from 'dayjs';
    import { fetchWrapper } from '@/helpers';
    import GlobalVariables from '../globals.js'

    const goBack = () => {
        router.go(-1)
    }

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
    const route = useRoute()
    const router = useRouter()

	async function fetchTripDetail() {
        fetchingTrip.value = true
        const id = route.params.tripid

        try {
            const tripInfoResponse = await fetchWrapper.get<trip[]>(GlobalVariables.apiURL + "tripinfo/?trip=" + id + "&fields=all")
            myTrip.value = tripInfoResponse[0]
        } catch(error) {
            console.error("Error fetching trip details:", error.message)
        }
        fetchingTrip.value = false
	}

	onMounted(async () => {
		await fetchTripDetail()
	})
</script>

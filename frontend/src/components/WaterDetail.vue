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
            {{ myWater.name }} ({{ myWater.water_type_text }})<br>
            {{ myWater.latitude }}, {{ myWater.longitude }}<br>
            {{ myWater.city.name }}, {{ myWater.state.abbr }}, {{ myWater.country.abbr }} ({{ myWater.county.name }} County)<br>
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

    const goBack = () => {
        router.go(-1)
    }

	interface water {
        id: number;
		name: string;
        water_type_text: string;
        latitude: number;
        longitude: number;
        city: { name: string };
        state: { abbr: string };
        country: { abbr: string };
        county: { name: string };
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
        city: { name: '' },
        state: { abbr: '' },
        country: { abbr: '' },
        county: { name: '' }
    })

    const launchList = ref([] as launch[])
	const fetchingWater = ref(false)
    const route = useRoute()
    const router = useRouter()

	async function fetchWaterDetail() {
        fetchingWater.value = true
        const id = route.params.waterid
		const waterInfoResponse = await axios.get<water[]>("http://localhost:8000/api/waterinfo/?water=" + id + "&fields=all")
        
        if (waterInfoResponse.data.length > 0) {
            myWater.value = waterInfoResponse.data[0]
        } else {
            console.error('Water not found')
        }

        // find launches on this body of water
		const launchInfoResponse = await axios.get<launch[]>("http://localhost:8000/api/launchinfo/?waterid=" + id)
		launchList.value = launchInfoResponse.data
        fetchingWater.value = false
	}

	onMounted(async () => {
		await fetchWaterDetail()
	})
</script>

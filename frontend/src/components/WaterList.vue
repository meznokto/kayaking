<template>
<div class="app">
	<div class="col-md-12">
	<div v-if="fetchingWaters">
		<h3>Loading...</h3>
	</div>
	<div v-else>
		<h3>{{ listMessage }}</h3>
	</div>
	</div>
	<div v-if="fetchingWaters">
		<b-spinner variant="primary" label="Loading"></b-spinner>
	</div>
	<div v-else class="row">
		<div class="col-md-12">
			<ul class="list-group">
				<li v-for="water in waterList" :key=water.id class="list-group-item">
					<router-link :to="{name: 'WaterDetail', params: { waterid: water.id }}">
					{{water.name}} - <div v-if="water.city !== null" style="display:inline;">{{water.city_name}}, </div>{{water.state_abbr}}, {{water.country_abbr}}</router-link>
				</li>
			</ul>
		</div>
	</div>
	<router-link v-if="authStore.accesstoken" :to="{name: 'CreateWater'}">Add a Body of Water</router-link>
	<div v-if="route.params.city || route.params.county || route.params.state || route.params.country">
		<button @click="clearFilters" class="btn btn-secondary mt-3">Clear Filters</button>
	</div>
</div>
</template>

<script setup lang="ts">
	import { ref, onMounted } from 'vue'
	import { useRoute } from 'vue-router';
	import { fetchWrapper } from '@/helpers';
	import GlobalVariables from '../globals.js'
	import { useAuthStore } from '@/stores';
	import CreateWater from './CreateWater.vue';

	const authStore = useAuthStore();

	interface water {
		id: number;
		name: string;
		city: number;
		city_name: string;
		county: number;
		county_name: string;
		state: number;
		state_name: string;
		state_abbr: string;
		country: number;
		country_name: string;
		country_abbr: string;
	}

	const route = useRoute();
	const waterList = ref([] as water[])
	const fetchingWaters = ref(false)
	const listMessage = ref("Loading...")
	let params = '?fields=all';

	if (typeof route.params.city !== 'undefined') {
		params += "&city=" + route.params.city;
	}
	else if (typeof route.params.county !== 'undefined') {
		params += "&county=" + route.params.county;
	}
	else if (typeof route.params.state !== 'undefined') {
		params += "&state=" + route.params.state;
	}
	else if (typeof route.params.country !== 'undefined') {
		params += "&country=" + route.params.country;
	}

	function clearFilters() {
		// clear our filters and reload the launch list
		params = ""
		if (typeof route.params.city !== 'undefined') {
			route.params.city = (function () { return; })();
		}
		if (typeof route.params.county !== 'undefined') {
			route.params.county = (function () { return; })();
		}
		if (typeof route.params.state !== 'undefined') {
			route.params.state = (function () { return; })();
		}
		if (typeof route.params.country !== 'undefined') {
			route.params.country = (function () { return; })();
		}

		fetchInitialWaters();
	}

	async function loadMoreWaters () {
		fetchingWaters.value = true

		try {
			const waterInfoResponse = await fetchWrapper.get<water[]>(GlobalVariables.apiURL + 'waterinfo/' + params)

			waterList.value.push(...(waterInfoResponse.data || []))
		} catch(error) {
			console.error("Error fetching more waters:", error.message)
		}
		fetchingWaters.value = false
	}

	async function fetchInitialWaters() {
		fetchingWaters.value = true

		try {
			const waterInfoResponse = await fetchWrapper.get<water[]>(GlobalVariables.apiURL + 'waterinfo/' + params)
			waterList.value = waterInfoResponse
		} catch(error) {
			console.error("Error fetching water list:", error.message)
		}
		listMessage.value = "Bodies of Water"

		if (typeof route.params.city !== 'undefined' && waterList.value[0].city !== null) {
			listMessage.value += " in " + waterList.value[0].city_name
		}
		else if (typeof route.params.county !== 'undefined' && waterList.value[0].county !== null) {
			listMessage.value += " in " + waterList.value[0].county_name + " County, "
			listMessage.value += waterList.value[0].state_name
		}
		else if (typeof route.params.state !== 'undefined' && waterList.value[0].state !== null) {
			listMessage.value += " in " + waterList.value[0].state_name
		}
		else if (typeof route.params.country !== 'undefined' && waterList.value[0].country !== null) {
			listMessage.value += " in " + waterList.value[0].country_name
		}

		fetchingWaters.value = false
	}

	onMounted(async () => {
		await fetchInitialWaters()
	});
</script>

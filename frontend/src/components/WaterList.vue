<template>
<div class="app">
	<div v-if="fetchingWaters">
		<p>Loading...</p>
	</div>
	<div v-else class="row">
		<div class="col-md-12">
			<h3>Bodies of Water</h3>
		</div>
		<div class="col-md-12">
			<ul class="list-group">
				<li v-for="water in waterList" :key=water.id class="list-group-item">
					<router-link :to="{name: 'WaterDetail', params: { waterid: water.id }}">
					{{water.name}} - {{water.city.name}}, {{water.state.abbr}}, {{water.country.abbr}}</router-link>
				</li>
			</ul>
		</div>
	</div>
	<div v-if="route.params.city || route.params.county || route.params.state || route.params.country">
		<button @click="clearFilters" class="btn btn-secondary mt-3">Clear Filters</button>
	</div>
</div>
</template>

<script setup lang="ts">
	import { ref, onMounted } from 'vue'
	import axios from 'axios'
	import { useRoute } from 'vue-router';
	import GlobalVariables from '../globals.js'

	interface water {
		id: number;
		name: string;
		city: { name: string };
		state: { abbr: string };
		country: { abbr: string };
	}

	const route = useRoute();
	const waterList = ref([] as water[])
	const fetchingWaters = ref(false)
	let params = '?';

	if (typeof route.params.city !== 'undefined') {
		params += "city=" + route.params.city;
	}
	else if (typeof route.params.county !== 'undefined') {
		params += "county=" + route.params.county;
	}
	else if (typeof route.params.state !== 'undefined') {
		params += "state=" + route.params.state;
	}
	else if (typeof route.params.country !== 'undefined') {
		params += "country=" + route.params.country;
	}

	function clearFilters() {
		// clear our filters and reload the launch list
		params = ""
		if (typeof route.params.city !== 'undefined') {
			route.params.city = null;
		}
		if (typeof route.params.county !== 'undefined') {
			route.params.county = null;
		}
		if (typeof route.params.state !== 'undefined') {
			route.params.state = null;
		}
		if (typeof route.params.state !== 'undefined') {
			route.params.country = null;
		}

		fetchInitialWaters();
	}

	async function loadMoreWaters () {
		fetchingWaters.value = true
		const waterInfoResponse = await axios.get<water[]>(GlobalVariables.apiURL + 'waterinfo/' + params)

		waterList.value.push(...(waterInfoResponse.data || []))
		fetchingWaters.value = false
	}

	async function fetchInitialWaters() {
		const waterInfoResponse = await axios.get<water[]>(GlobalVariables.apiURL + 'waterinfo/' + params)
		waterList.value = waterInfoResponse.data
	}

	onMounted(async () => {
		await fetchInitialWaters()
	})
</script>

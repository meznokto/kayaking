<template>
<div class="app">
	<div v-if="route.params.city || route.params.county || route.params.state || route.params.country" class="col-md-12">
		<h3>Filtered Boat Launches</h3>
	</div>
	<div v-else class="col-md-12">
		<h3>Latest Boat Launches</h3>
	</div>
	<div v-if="fetchingLaunches">
		<b-spinner variant="primary" label="Loading"></b-spinner>
	</div>
	<div v-else class="row">
		<div class="col-md-12">
			<ul class="list-group">
				<li v-for="launch in launchList" :key=launch.id class="list-group-item">
					<div class="container-flued">
						<div class="row">
							<div class="col-sm-1">
								<router-link :to="{name: 'LaunchDetail', params: { launchid: launch.id }}">
								<div v-if="launch.thumbnail">
									<img v-bind:src="GlobalVariables.imgURL + launch.thumbnail" alt="Launch Image" class="img-fluid">
								</div>
								<div v-else>
									<img v-bind:src="GlobalVariables.imgURL + '/static/default_launch_thumbnail.png'" alt="Default Launch Image" class="img-fluid">
								</div>
								</router-link>
							</div>
							<div class="col-sm-10">
								<router-link :to="{name: 'LaunchDetail', params: { launchid: launch.id }}">
									{{launch.name}}
								</router-link><br>
								<router-link :to="{name: 'WaterDetail', params: { waterid: launch.body_of_water.id }}">
									{{ launch.body_of_water.name}}
								</router-link><br>
									{{launch.city.name}}, {{launch.state.abbr}}, {{launch.country.abbr}}
							</div>
						</div>
					</div>
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
	import { routerViewLocationKey, useRoute } from 'vue-router'
	import { fetchWrapper } from '@/helpers';
	import GlobalVariables from '../globals.js'

	interface launch {
		id: number;
		name: string;
		city: { name: string };
		state: { abbr: string };
		country: { abbr: string };
		body_of_water: { id: number; name: string };
		thumbnail: string;
	}

	const route = useRoute();
	const launchList = ref([] as launch[])
	const fetchingLaunches = ref(false)
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

		fetchInitialLaunches();
	}

	async function loadMoreLaunches () {
		fetchingLaunches.value = true

		try {
			const launchInfoResponse = await fetchWrapper.get<trip[]>(GlobalVariables.apiURL + 'launchinfo/' + params)
			launchList.value.push(...(launchInfoResponse.data || []))
		} catch(error) {
			console.error("Error fetching more launches:", error.message)
		}
		fetchingLaunches.value = false
	}

	async function fetchInitialLaunches() {
		fetchingLaunches.value = true

		try {
			const launchInfoResponse = await fetchWrapper.get<trip[]>(GlobalVariables.apiURL + 'launchinfo/' + params)
			launchList.value = launchInfoResponse
		} catch(error) {
			console.error("Error fetching initial launches:", error.message)
		}
		fetchingLaunches.value = false
	}

	onMounted(async () => {
		await fetchInitialLaunches()
	})
</script>

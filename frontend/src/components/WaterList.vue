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
</div>
</template>

<script setup lang="ts">
	import { ref, onMounted } from 'vue'
	import axios from 'axios'
	import GlobalVariables from '../globals.js'

	interface water {
		id: number;
		name: string;
		city: { name: string };
		state: { abbr: string };
		country: { abbr: string };
	}

	const waterList = ref([] as water[])
	const fetchingWaters = ref(false)

	async function loadMoreWaters () {
		fetchingWaters.value = true
		const waterInfoResponse = await axios.get<water[]>(GlobalVariables.apiURL + 'waterinfo/')

		waterList.value.push(...(waterInfoResponse.data || []))
		fetchingWaters.value = false
	}

	async function fetchInitialWaters() {
		const waterInfoResponse = await axios.get<water[]>(GlobalVariables.apiURL + 'waterinfo/')
		waterList.value = waterInfoResponse.data
	}

	onMounted(async () => {
		await fetchInitialWaters()
	})
</script>

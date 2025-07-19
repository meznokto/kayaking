<template>
	<div class="row">
		<div class="col-md-12">
			<h3>Launches</h3>
		</div>
		<div class="col-md-12">
			<ul class="list-group">
				<li v-for="launch in launchInfo" :key=launch.id class="list-group-item">
					<a :href="'#/launchdetail/?launch=' + launch.id">
					{{launch.name}} - {{launch.city.name}}, {{launch.state.abbr}}, {{launch.country.abbr}}</a>
				</li>
			</ul>
		</div>
	</div>
</template>

<script setup lang="ts">
	import { ref, onMounted } from 'vue'
	import axios from 'axios'

	interface launch {
		id: number;
		name: string;
		city: { name: string };
		state: { abbr: string };
		country: { abbr: string };
	}
	const launchInfo = ref([] as launch[])
	const fetchingLaunches = ref(false)
	async function loadMoreLaunches () {
		fetchingLaunches.value = true
		const launchInfoResponse = await axios.get<launch[]>('http://localhost:8000/api/launchinfo/')
		launchInfo.value.push(...(launchInfoResponse.data || []))

		fetchingLaunches.value = false
	}

	async function fetchInitialLaunches() {
		const launchInfoResponse = await axios.get<launch[]>('http://localhost:8000/api/launchinfo/')
		launchInfo.value = launchInfoResponse.data
	}

	onMounted(async () => {
		await fetchInitialLaunches()
	})
</script>

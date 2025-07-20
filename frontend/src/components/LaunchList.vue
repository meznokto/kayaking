<template>
<div class="app">
	<div v-if="fetchingLaunches">
		<p>Loading...</p>
	</div>
	<div v-else class="row">
		<div class="col-md-12">
			<h3>Boat Launches</h3>
		</div>
		<div class="col-md-12">
			<ul class="list-group">
				<li v-for="launch in launchList" :key=launch.id class="list-group-item">
					<div class="container-flued">
						<div class="row">
							<div class="col-sm-1">
								<router-link :to="{name: 'LaunchDetail', params: { launchid: launch.id }}">
								<div v-if="launch.thumbnail">
									<img v-bind:src="'http://localhost:8000' + launch.thumbnail" alt="Launch Image" class="img-fluid">
								</div>
								<div v-else>
									<img src="http://localhost:8000/static/default_launch_thumbnail.png" alt="Default Launch Image" class="img-fluid">
								</div>
								</router-link>
							</div>
							<div class="col-sm-10">
								<router-link :to="{name: 'LaunchDetail', params: { launchid: launch.id }}">
									{{launch.name}}
								</router-link><br>
								{{launch.city.name}}, {{launch.state.abbr}}, {{launch.country.abbr}}
							</div>
						</div>
					</div>
				</li>
			</ul>
		</div>
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
		thumbnail: string;
	}

	const launchList = ref([] as launch[])
	const fetchingLaunches = ref(false)

	async function loadMoreLaunches () {
		fetchingLaunches.value = true
		const launchInfoResponse = await axios.get<launch[]>('http://localhost:8000/api/launchinfo/')

		launchList.value.push(...(launchInfoResponse.data || []))
		fetchingLaunches.value = false
	}

	async function fetchInitialLaunches() {
		const launchInfoResponse = await axios.get<launch[]>('http://localhost:8000/api/launchinfo/')
		launchList.value = launchInfoResponse.data
	}

	onMounted(async () => {
		await fetchInitialLaunches()
	})
</script>

<template>
	<div class="row">
		<div class="col-md-12">
			<h3>Bodies of Water</h3>
		</div>
		<div class="col-md-12">
			<ul class="list-group">
				<li v-for="water in waterList" :key=water.id class="list-group-item">
					<a :href="'#/waterdetail/?water=' + water.id">
					{{water.name}} - {{water.city.name}}, {{water.state.abbr}}, {{water.country.abbr}}</a>
				</li>
			</ul>
		</div>
	</div>
</template>

<script setup lang="ts">
	import { ref, onMounted } from 'vue'
	import axios from 'axios'

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
		const waterInfoResponse = await axios.get<water[]>('http://localhost:8000/api/waterinfo/')

		waterList.value.push(...(waterInfoResponse.data || []))
		fetchingWaters.value = false
	}

	async function fetchInitialWaters() {
		const waterInfoResponse = await axios.get<water[]>('http://localhost:8000/api/waterinfo/')
		waterList.value = waterInfoResponse.data
	}

	onMounted(async () => {
		await fetchInitialWaters()
	})
</script>

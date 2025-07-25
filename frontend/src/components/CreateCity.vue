<template>
    <form @submit.prevent="submitForm">
        <div>
            <label for="name">City Name:</label>
            <input type="text" id="name" v-model="formData.name" required />
        </div>
        <div>
            <select id="country" v-model="selectedCountry" @change="fetchStates">
                <option v-for="country in countries" :key="country.id" :value="country.id">{{ country.name }}</option>
            </select>
            <select id="state" v-model="formData.state" @change="fetchCounties">
                <option v-for="state in states" :key="state.id" :value="state.id">{{ state.name }}</option>
            </select>
            <select id="county" v-model="formData.county" @change="fetchCities">
                <option v-for="county in counties" :key="county.id" :value="county.id">{{ county.name }}</option>
            </select>
            <!-- <select v-model="selectedCity">
                <option v-for="city in cities" :key="city.id" :value="city.id">{{ city.name }}</option>
            </select> -->
        </div>
        <button type="submit">Add City</button>
    </form>
</template>

<script>
import { fetchWrapper } from '@/helpers';
import GlobalVariables from '../globals.js';

export default{
  data() {
    return {
        formData: {
            name: '',
            county: 0,
            state: 0,
        },
      countries: [],
      states: [],
      counties: [],
      cities: [],
      selectedCountry: null,
      selectedState: null,
      selectedCounty: null,
      selectedCity: null,
    };
  },
  mounted() {
    this.fetchCountries();
  },
  methods: {
    async fetchCountries() {
      this.countries = await fetchWrapper.get(GlobalVariables.apiURL + 'util/countries/');
    },
    async fetchStates() {
      this.states = await fetchWrapper.get(GlobalVariables.apiURL + `util/states/?country=${this.selectedCountry}`);
      this.counties = [];
      this.cities = [];
      this.selectedState = null;
      this.selectedCounty = null;
      this.selectedCity = null;
    },
    async fetchCounties() {
      this.counties = await fetchWrapper.get(GlobalVariables.apiURL + `util/counties/?state=${this.formData.state}`);
      this.cities = [];
      this.selectedCounty = null;
      this.selectedCity = null;
    },
    async fetchCities() {
      this.cities = await fetchWrapper.get(GlobalVariables.apiURL + `util/cities/?county=${this.formData.county}`);
      this.selectedCity = null;
    },
    async submitForm() {
        try {
            const response = await fetchWrapper.post(GlobalVariables.apiURL + 'util/cities/', this.formData)
            console.log("POST response:" + resposne)
        } catch(error) {

        }
    },
  },
};
</script>
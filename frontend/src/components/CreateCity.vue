<template>
    <b-form @submit.prevent="submitForm">
        <b-form-group label="City Name">
            <b-form-input id="name" v-model="formData.name" type="text" required></b-form-input>
        </b-form-group>
        <b-form-group label="Country">
            <b-form-select id="country" v-model="selectedCountry" @change="fetchStates">
                <option v-for="country in countries" :key="country.id" :value="country.id">{{ country.name }}</option>
            </b-form-select>
        </b-form-group>
        <b-form-group label="State">
            <b-form-select id="state" v-model="formData.state" @change="fetchCounties">
                <option v-for="state in states" :key="state.id" :value="state.id">{{ state.name }}</option>
            </b-form-select>
        </b-form-group>
        <b-form-group label="County">
            <b-form-select id="county" v-model="formData.county">
                <option v-for="county in counties" :key="county.id" :value="county.id">{{ county.name }}</option>
            </b-form-select>
        </b-form-group>
        <button type="submit">Add City</button>
    </b-form>
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
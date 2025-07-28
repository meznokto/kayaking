<template>
    <b-form @submit.prevent="submitForm">
        <b-form-group label="Water Name">
            <b-form-input id="name" v-model="formData.name" type="text" required></b-form-input>
        </b-form-group>
        <b-form-group label="Country">
            <b-form-select id="country" v-model="formData.country" @change="fetchStates">
                <option v-for="country in countries" :key="country.id" :value="country.id">{{ country.name }}</option>
            </b-form-select>
        </b-form-group>
        <b-form-group label="State">
            <b-form-select id="state" v-model="formData.state" @change="fetchCounties">
                <option v-for="state in states" :key="state.id" :value="state.id">{{ state.name }}</option>
            </b-form-select>
        </b-form-group>
        <b-form-group label="County">
            <b-form-select id="county" v-model="formData.county" @change="fetchCities">
                <option v-for="county in counties" :key="county.id" :value="county.id">{{ county.name }}</option>
            </b-form-select>
        </b-form-group>
        <b-form-group label="City">
            <b-form-select id="city" v-model="formData.city">
                <option v-for="city in cities" :key="city.id" :value="city.id">{{ city.name }}</option>
            </b-form-select>
        </b-form-group>
        <b-form-group>
            Latitude: <b-form-input id="latitude" v-model="formData.latitude" type="text"></b-form-input>
            Longitude: <b-form-input id="longitude" v-model="formData.longitude" type="text"></b-form-input>
        </b-form-group>
        <button type="submit">Add Water</button>
        <div v-if="showSuccessMessage">Successfully added city.</div>
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
            country: 0,
            county: 0,
            state: 0,
            city: 0,
            latitude: 0,
            longitude: 0,
        },
      countries: [],
      states: [],
      counties: [],
      cities: [],
      showSuccessMessage: false,
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
      this.states = await fetchWrapper.get(GlobalVariables.apiURL + `util/states/?country=${this.formData.country}`);
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
            const response = await fetchWrapper.post(GlobalVariables.apiURL + 'waterinfo/', this.formData)
            
            this.showSuccessMessage = true
            this.formData.name = '';
            this.formData.county = 0;
            this.formData.state = 0;
            setTimeout(() => {
                this.showSuccessMessage = false;
            }, 3000);
            router.push('/waterlist/');
        } catch(error) {

        }
    },
  },
};
</script>
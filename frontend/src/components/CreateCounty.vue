<template>
    <b-form @submit.prevent="submitForm">
        <b-form-group label="County Name">
            <b-form-input id="name" v-model="formData.name" type="text" required></b-form-input>
        </b-form-group>
        <b-form-group label="Country">
            <b-form-select id="country" v-model="selectedCountry" @change="fetchStates">
                <option v-for="country in countries" :key="country.id" :value="country.id">{{ country.name }}</option>
            </b-form-select>
        </b-form-group>
        <b-form-group label="State">
            <b-form-select id="state" v-model="formData.state">
                <option v-for="state in states" :key="state.id" :value="state.id">{{ state.name }}</option>
            </b-form-select>
        </b-form-group>

        <button type="submit">Add County</button>
        <div v-if="showSuccessMessage">Successfully added county.</div>
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
            state: 0,
        },
      countries: [],
      states: [],
      selectedCountry: null,
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
      this.states = await fetchWrapper.get(GlobalVariables.apiURL + `util/states/?country=${this.selectedCountry}`);
      this.counties = [];
      this.cities = [];
      this.selectedState = null;
      this.selectedCounty = null;
      this.selectedCity = null;
    },
    async submitForm() {
        try {
            const response = await fetchWrapper.post(GlobalVariables.apiURL + 'util/counties/', this.formData)
            this.showSuccessMessage = true
            this.formData.name = '';
            this.formData.state = 0;
            setTimeout(() => {
                this.showSuccessMessage = false;
            }, 3000);
        } catch(error) {

        }
    },
  },
};
</script>
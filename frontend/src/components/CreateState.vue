<template>
    <b-form @submit.prevent="submitForm">
        <b-form-group label="State Name">
            <b-form-input id="name" v-model="formData.name" type="text" required></b-form-input>
        </b-form-group>
        <b-form-group label="Abbreviation">
            <b-form-input id="abbr" v-model="formData.abbr" type="text" required></b-form-input>
        </b-form-group>
        <b-form-group label="Country">
            <b-form-select id="country" v-model="formData.country">
                <option v-for="country in countries" :key="country.id" :value="country.id">{{ country.name }}</option>
            </b-form-select>
        </b-form-group>
        <button type="submit">Add State</button>
        <div v-if="showSuccessMessage">Successfully added state.</div>
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
            abbr: '',
            country: 0,
        },
      countries: [],
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

    async submitForm() {
        try {
            const response = await fetchWrapper.post(GlobalVariables.apiURL + 'util/states/', this.formData)
            
            this.showSuccessMessage = true
            this.formData.name = '';
            this.formData.abbr = '';
            setTimeout(() => {
                this.showSuccessMessage = false;
            }, 3000);
        } catch(error) {

        }
    },
  },
};
</script>
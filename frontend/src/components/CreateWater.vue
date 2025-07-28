<template>
    <b-form @submit.prevent="submitForm">
        <b-form-group label="Water Name">
            <b-form-input id="name" v-model="formData.name" type="text" required></b-form-input>
        </b-form-group>
        <b-form-group label="Country">
            <b-form-select id="country" v-model="formData.country" @change="fetchStates" required>
                <option v-for="country in countries" :key="country.id" :value="country.id">{{ country.name }}</option>
            </b-form-select>
        </b-form-group>
        <b-form-group label="State">
            <b-form-select id="state" v-model="formData.state" @change="fetchCounties" required>
                <option v-for="state in states" :key="state.id" :value="state.id">{{ state.name }}</option>
            </b-form-select>
        </b-form-group>
        <b-form-group label="County">
            <b-form-select id="county" v-model="formData.county" @change="fetchCities" required>
                <option v-for="county in counties" :key="county.id" :value="county.id">{{ county.name }}</option>
            </b-form-select>
        </b-form-group>
        <b-form-group label="City">
            <b-form-select id="city" v-model="formData.city">
                <option v-for="city in cities" :key="city.id" :value="city.id">{{ city.name }}</option>
            </b-form-select>
        </b-form-group>
        <b-form-group>
            Latitude: <b-form-input id="latitude" v-model="formData.latitude" type="number" required></b-form-input>
            Longitude: <b-form-input id="longitude" v-model="formData.longitude" type="number" required></b-form-input>
        </b-form-group>
        <b-form-group label="Type of water">
            <b-form-radio v-model="formData.water_type" value="0">River</b-form-radio>
            <b-form-radio v-model="formData.water_type" value="1">Lake</b-form-radio>
            <b-form-radio v-model="formData.water_type" value="2">Resivoir</b-form-radio>
            <b-form-radio v-model="formData.water_type" value="3">Other</b-form-radio>
        </b-form-group>
        <b-form-group label="Size">
          <b-container fluid>
            <b-row class="my-1">
              <b-col sm="2">
                <label for="acres">Acres</label>
              </b-col>
              <b-col sm="10">
                <b-form-input id="acres" v-model="formData.acres" @change="updateHectares" type="number"></b-form-input>
              </b-col>
            </b-row>
            <b-row class="my-1">
              <b-col sm="2">
                <label for="hectares">Hectares</label>
              </b-col>
              <b-col sm="10">
                <b-form-input id="hectares" v-model="formData.hectares" type="number"></b-form-input>
              </b-col>
            </b-row>
          </b-container>
        </b-form-group>
        <b-form-group label="Depth">
          <b-container fluid>
            <b-row class="my-1">
              <b-col sm="2">
                <label for="max_depth_feet">Feet</label>
              </b-col>
              <b-col sm="10">
                <b-form-input id="max_depth_feet" v-model="formData.max_depth_feet" type="number"></b-form-input>
              </b-col>
              <b-col sm="2">
                <label for="max_depth_meters">Meters</label>
              </b-col>
              <b-col sm="10">
                <b-form-input id="max_depth_meters" v-model="formData.max_depth_meters" type="number"></b-form-input>
              </b-col>
            </b-row>
          </b-container>
        </b-form-group>
        <b-form-group>
          <b-form-textarea id="description" v-model="formData.description" rows=8 placeholder="Description..."></b-form-textarea>
        </b-form-group>
        <button type="submit">{{ buttonText }}</button>
        <div v-if="showSuccessMessage">Successfully added water.</div>
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
            water_type: 0,
            acres: 0,
            hectares: 0,
            max_depth_feet: 0,
            max_depth_meters: 0,
            description: '',
        },
      countries: [],
      states: [],
      counties: [],
      cities: [],
      showSuccessMessage: false,
      buttonText: 'Add Water',
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
    async updateHectares() {
      this.formData.hectares = this.formData.acres * 0.404;
    },
    async submitForm() {
      this.buttonText = 'Submitting...';
      
      try {
        const response = await fetchWrapper.post(GlobalVariables.apiURL + 'waterinfo/', this.formData)
            
        this.showSuccessMessage = true
        this.formData.name = '';
        this.formData.county = 0;
        this.formData.state = 0;
        this.buttonText = 'Success!';
        setTimeout(() => {
          this.showSuccessMessage = false;
          this.buttonText = 'Add Water';
        }, 3000);
        router.push('/waterlist/');
        } catch(error) {

        }

        this.isSubmitting = false;
    },
  },
};
</script>
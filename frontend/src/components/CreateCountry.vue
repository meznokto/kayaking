<template>
    <b-form @submit.prevent="submitForm">
        <b-form-group label="Country Name">
            <b-form-input id="name" v-model="formData.name" type="text" required></b-form-input>
        </b-form-group>
        <b-form-group label="Abbreviation">
            <b-form-input id="abbr" v-model="formData.abbr" type="text" required></b-form-input>
        </b-form-group>
        <button type="submit">Add Country</button>
        <div v-if="showSuccessMessage">Successfully added country.</div>
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
        },
      showSuccessMessage: false,
    };
  },
  mounted() {
    
  },
  methods: {
    async submitForm() {
        try {
            const response = await fetchWrapper.post(GlobalVariables.apiURL + 'util/countries/', this.formData)
            
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
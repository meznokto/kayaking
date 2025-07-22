import { defineStore } from 'pinia';
import { fetchWrapper } from '@/helpers';
import GlobalVariables from '../globals.js'

const baseUrl = GlobalVariables.apiURL + 'users/';

export const useUsersStore = defineStore('users', {
    //id: 'users',
    state: () => ({
        users: {}
    }),
    actions: {
        async getAll() {
            this.users = { loading: true };
            fetchWrapper.get(baseUrl)
                .then(users => this.users = users)
                .catch(error => this.users = { error })
        }
    }
});
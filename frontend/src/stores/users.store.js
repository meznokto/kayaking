import { defineStore } from 'pinia';

import { fetchWrapper } from '@/helpers';

const baseUrl = `http://localhost:8000/api/users/`;

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
            console.log("Users fetched:", this.users);
        }
    }
});
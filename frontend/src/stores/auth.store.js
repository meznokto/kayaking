import { defineStore } from 'pinia';

import { fetchWrapper } from '@/helpers';

import router from '../routes'

const baseUrl = `http://localhost:8000/api/token/`;

export const useAuthStore = defineStore('auth', {
    //id: 'auth',
    state: () => ({
        data: null,
        accesstoken: null,
        refreshtoken: null,
        refreshTokenTimeout: null
    }),
    actions: {
        async login(email, password) {
            this.data = await fetchWrapper.post(`${baseUrl}`, { email, password }, { credentials: 'include' });
            //console.log(this.data);
            this.accesstoken = this.data.access;
            this.refreshtoken = this.data.refresh;
            console.log("Access Token:", this.accesstoken);
            console.log("Refresh Token:", this.refreshtoken);
            // start the timer to refresh the token before it expires
            this.startRefreshTokenTimer();
        },
        logout() {
            console.log("Logging out...");
            //fetchWrapper.post(`${baseUrl}revoke-token/`, {}, { credentials: 'include' });
            this.stopRefreshTokenTimer();
            this.accesstoken = null;
            this.refreshtoken = null;
            router.push('/login');
        },
        async refreshToken() {
            console.log("Refreshing token...");
            this.data = await fetchWrapper.post(`${baseUrl}refresh/`, {}, { credentials: 'include' });
            this.accesstoken = this.data.access;
            this.refreshtoken = this.data.refresh;
            console.log("Refreshed Access Token:", this.accesstoken);
            console.log("Refreshed Refresh Token:", this.refreshtoken);
            // reset the timer to refresh the token before it expires
            this.startRefreshTokenTimer();
        },
        startRefreshTokenTimer() {
            //const expires = new Date();
            const timeout = Date.now() + (60 * 1000);
            console.log("Setting refresh token timeout for:", timeout);
            this.refreshTokenTimeout = setTimeout(this.refreshToken, timeout);
        },    
        stopRefreshTokenTimer() {
            clearTimeout(this.refreshTokenTimeout);
        }
    }
});
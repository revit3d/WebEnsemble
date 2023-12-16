import { defineStore } from 'pinia';

export const useStore = defineStore('main', {
    state: () => {
        return {
            modelStates: null,
            API_URL_CLIENT: 'localhost',
            API_URL_SERVER: 'backend-api:8000',
        }
    },
    actions: {
        async fetchData() {
            try {
                const apiUrl = process.server ? this.API_URL_SERVER : this.API_URL_CLIENT
                const response = await $fetch('http://' + apiUrl + '/api/models/list');
                this.modelStates = response.models;
            } catch (error) {
                console.error('Error fetching data:', error);
            }
        }
    }
});
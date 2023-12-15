import { defineStore } from 'pinia';

export const useStore = defineStore('main', {
    state: () => {
        return {
            modelStates: null
        }
    },
    actions: {
        async fetchData() {
            try {
                const response = await $fetch('http://localhost:8000/models/list');
                this.modelStates = response.models;
            } catch (error) {
                console.error('Error fetching data:', error);
            }
        }
    }
});
import { createStore } from 'vuex';

export const store = createStore({
    state() {
        return {
            modelStates: null
        }
    },
    mutations: {
        updateModelState(state, modelState) {
            state.modelStates[modelState.id] = modelState;
        },
        updateModelStates(state, newStates) {
            state.modelStates = newStates;
        }
    },
    actions: {
        async fetchData({ commit }) {
            console.log('fetching start data')
            try {
                const response = await $fetch('http://localhost:8000/models/list');
                commit('updateModelStates', response.models);
            } catch (error) {
                console.error('Error fetching data:', error);
            }
        }
    }
});
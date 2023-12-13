<template>
  <div class="background">
    <Header />
    <router-view class="p-20"></router-view>
    <Footer />
  </div>
</template>

<script>
  import Header from '@/components/Header.vue';
  import Footer from '@/components/Footer.vue';
  import { store } from '@/store';

export default {
  components: {
    Header,
    Footer,
  },
  async mounted() {
    const websocket = new WebSocket('ws://localhost:8000/model/fit');
    store.dispatch('fetchData');

    websocket.onmessage = async (event) => {
      console.log(event);
      console.log('model fitted: ' + modelId);
      try {
        const updatedModelState = await $fetch('http://localhost:8000/model/' + modelId);
        store.commit('updateModelState', updatedModelState);
      } catch (error) {
        console.error('Error fetching data:', error);
        throw error;
      }
    }
  }
};
</script>

<style scoped>
.background {
  background: rgb(105,255,251);
  background: linear-gradient(153deg, rgba(105,255,251,1) 0%, rgba(173,145,255,1) 100%);
}
</style>
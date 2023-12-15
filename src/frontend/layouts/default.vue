<template>
  <div class="grid content-between" style="min-height: 100vh">
    <Header />
    <router-view class="p-20"></router-view>
    <Footer />
  </div>
</template>

<script>
import Header from '@/components/Header.vue';
import Footer from '@/components/Footer.vue';
import { useStore } from '@/store';

export default defineNuxtComponent({
  components: {
    Header,
    Footer,
  },
  asyncData: async () =>  {
    const store = useStore();
    await store.fetchData();
    return {}
  },
  mounted() {
    const store = useStore();
    const apiUrl = process.server ? store.API_URL_SERVER : store.API_URL_CLIENT
    const websocket = new WebSocket('ws://' + apiUrl + '/model/fit');

    websocket.onmessage = ({ data }) => {
      const store = useStore();
      const newModelState = JSON.parse(data);
      store.modelStates = store.modelStates.map((model) => {
        if (model.id == newModelState.id) { return newModelState; }
        return model;
      })
    }
  }
});
</script>

<style>
body, html {
  min-height: 100vh;
  margin: 0;
  padding: 0;
  background: rgb(105,255,251);
  background: linear-gradient(153deg, rgb(214, 253, 252) 0%, rgb(231, 224, 255) 100%);
}
</style>
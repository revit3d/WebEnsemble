<template>
  <aside :class="{ 'w-1/3': isOpen, 'w-0': !isOpen }" class="fixed top-0 left-0 bg-gray-800 text-white transition-all overflow-x-hidden h-full">
    <div class="ml-4">
      <h1 class="text-3xl font-semibold tracking-wide text-cyan-700 mb-8 ml-16 mt-5">Model explorer</h1>
      <div class="text-2xl text-emerald-600 space-y-4 ml-6">
        <button class="new-model-button" @click="redirectNew()">New model</button>
        <ul v-for="model in modelStates">
          <li>
            <button @click="redirectModel(model[0])">{{ model[1] }}</button>
            <span :class="['dot-container', {'dot-green': isModelFitted(model[2]), 'dot-yellow': isModelFitting(model[2], model[3]), 'dot-red': !isModelFitting(model[2], model[3])}, 'ml-2']"></span>
          </li>
        </ul>
      </div>
    </div>
  </aside>
</template>

<script>
import { store } from '@/store';

  export default defineNuxtComponent ({
    props: {
      isOpen: Boolean,
    },
    computed: {
      modelStates() {
        return store.state.modelStates;
      }
    },
    methods: {
      toggleSidebar() {
        props.isOpen = false;
      },
      async redirectModel(model_uuid) {
        await navigateTo('/model/' + model_uuid);
        location.reload();
      },
      async redirectNew() {
        await navigateTo('/model/new');
        location.reload();
      },
      isModelFitted(is_trained) {
        return is_trained;
      },
      isModelFitting(is_trained, target_name) {
        return (target_name !== null) && !is_trained;
      },
    },
});
</script>

<style scoped>
@import '@/assets/DotStyle.css';

.new-model-button {
  background-color: transparent;
  border: 2px dashed white;
  border-radius: 10px;
  color: white;
  padding: 10px 20px;
  text-align: center;
  display: inline-block;
  cursor: pointer;
}
</style>
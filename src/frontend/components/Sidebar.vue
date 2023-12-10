<template>
  <aside :class="{ 'w-1/3': isOpen, 'w-0': !isOpen }" class="fixed top-0 left-0 bg-gray-800 text-white transition-all overflow-x-hidden h-full">
    <div class="ml-4">
      <h1 class="text-2xl font-semibold tracking-wide mb-4 ml-16 mt-5">Model explorer</h1>
      <ul class="text-blue-500">
          <li class="mb-2"><NuxtLink to="/model/fit/1" @click="toggleSidebar">Model 1</NuxtLink></li>
          <li class="mb-2"><NuxtLink to="/model/fit/2">Model 2</NuxtLink></li>
          <li class="mb-2"><NuxtLink to="/model/fit/3">Model 3</NuxtLink></li>
      </ul>
    </div>
  </aside>
</template>

<script>
  export default {
    props: {
      isOpen: Boolean,
    },
    methods: {
      toggleSidebar() {
        console.log('here');
        this.isSidebarOpen = false;
      },
    },
  };
</script>

<style scoped>
</style>
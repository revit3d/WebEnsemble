<template>
    <aside :class="{ 'w-1/3': isOpen, 'w-0': !isOpen }" class="bg-gray-800 text-white transition-all overflow-x-hidden absolute h-full">
      <div class="ml-4">
        <h1 class="text-2xl font-semibold tracking-wide mb-4 ml-16 mt-5">Model explorer</h1>
        <ul>
            <li class="mb-2"><router-link to="/link1" class="text-blue-500">Model 1</router-link></li>
            <li class="mb-2"><router-link to="/link2" class="text-blue-500">Model 2</router-link></li>
            <li class="mb-2"><router-link to="/link3" class="text-blue-500">Model 3</router-link></li>
        </ul>
      </div>
    </aside>
  </template>
  
  <script>
  export default {
    props: {
        isOpen: Boolean,
    },
  };
  </script>
  
  <style scoped>
  </style>
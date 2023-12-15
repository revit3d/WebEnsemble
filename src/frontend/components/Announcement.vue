<template>
  <div class="announcement-container">
    <div class="announcement">
      <p class="text-5xl font-bold tracking-widest m-3">Model is not selected</p>
      <p class="text-5xl font-medium tracking-wider m-px">Select a model from the sidebar</p>
      <p class="text-5xl font-medium tracking-wider">or <NuxtLink to="/model/new" class="text-decoration: underline text-cyan-900">create a new one</NuxtLink></p>
    </div>
  </div>
</template>

<script>
export default {
};
</script>

<style scoped>
.announcement-container {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 100vw;
  height: 70vh;
}

.announcement {
  text-align: center;
  padding: 30px;
  border: 3px solid #0891b2;
  border-radius: 8px;
  background-color: #bae6fd;
}
</style>
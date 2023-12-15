<template>
  <div>
    <h1>This is the Home Page</h1>
  </div>
</template>

<script setup>
  await navigateTo('/home');
  location.reload();
</script>
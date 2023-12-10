<template>
    <div class="fixed top-0 right-0 p-6">
      <Logo />
    </div>
    <div class="flex h-screen">
      <Sidebar :isOpen="isSidebarOpen" />

      <SidebarButton @toggle-sidebar="toggleSidebar" />
  
      <router-view class="flex-1 p-10"></router-view>
    </div>
    <div><Footer /></div>
  </template>
  
  <script>
  import Logo from '@/components/Logo.vue'
  import Sidebar from '@/components/Sidebar.vue';
  import SidebarButton from '@/components/SidebarButton.vue';
  import Footer from '@/components/Footer.vue';
  
  export default {
    components: {
      Logo,
      Sidebar,
      SidebarButton,
      Footer,
    },
    data() {
      return {
        isSidebarOpen: false,
      };
    },
    methods: {
      toggleSidebar() {
        this.isSidebarOpen = !this.isSidebarOpen;
      },
    },
  };
  </script>
  
  <style scoped>
    body, #app {
      user-select: none;
      background-color: #99f6e4
    }
  </style>
<template>
    <header class="header bg-gray-800">
        <Logo class="fixed right-6 top-6"/>

        <div>
            <Sidebar :isOpen="isSidebarOpen" />
            <SidebarButton @toggle-sidebar="toggleSidebar" />
        </div>
    </header>
</template>

<script>
    import Logo from './Logo.vue'
    import Sidebar from './Sidebar.vue';
    import SidebarButton from './SidebarButton.vue';

    export default {
        components: {
            Logo,
            Sidebar,
            SidebarButton,
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
    }
</script>

<style scoped>
.header {
    left: 0;
    top: 0;
    height: 6vh;
    position: fixed;
    width: 100vw;
    user-select: none;
    z-index: 100;
}
</style>
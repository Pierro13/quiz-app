<script setup>
import { RouterView } from 'vue-router'
import Navbar from '@/views/Navbar.vue';
</script>

<template>
  <div id="app">
    <Navbar />
    <router-view></router-view>
  </div>
</template>

<style>
/* Ajoutez des styles si nécessaire */
</style>



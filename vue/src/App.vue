<script setup>
import SiteHeader from './components/SiteHeader.vue';
import SiteFooter from './components/SiteFooter.vue';
</script>

<template>
  <SiteHeader />
  <main class="container-page" style="padding-top: 2.5rem; padding-bottom: 2.5rem;">
    <router-view :key="$route.fullPath" />
  </main>
  <SiteFooter />
</template>
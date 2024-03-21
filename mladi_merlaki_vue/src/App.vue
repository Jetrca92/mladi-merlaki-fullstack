<template>
  <div id="wrapper">
    
  </div>
  
  <NavBar />

  
  <router-view/>
  
  
  

  <footer class="footer">
    <p class="has-text-centered">Copyright (c) 2024 @Jetrca92</p>
  </footer>
</template>

<script setup>
import NavBar from './components/NavBar.vue';
import HomeView from './views/HomeView.vue';
</script>
<style lang="scss">
@import '../node_modules/bulma/';
</style>

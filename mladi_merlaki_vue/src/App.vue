<template>
  <div id="wrapper">
    
  </div>
  
  <NavBar />

  
  <router-view/>
  
  
  

  <footer class="footer">
    <p class="has-text-centered">
      Data provided by<a href="https://site.financialmodelingprep.com/" target="_blank">Financial Modeling Prep</a> 
      and <a href="https://www.coingecko.com/" target="_blank">CoinGecko</a>
    </p>
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

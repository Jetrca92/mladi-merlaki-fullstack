<script setup>
import axios from 'axios'
import { ref } from 'vue'
import { useStore } from 'vuex'
import { useRouter } from 'vue-router'

const showMobileMenu = ref(false)
const store = useStore()
const router = useRouter()
const toggleMobileMenu = () => {
  showMobileMenu.value = !showMobileMenu.value
}
const logout = () => {
  axios.defaults.headers.common["Authorization"] = ""

  localStorage.removeItem("token")
  localStorage.removeItem("username")
  localStorage.removeItem("userid")

  store.commit('removeToken')

  router.push('/')
}
</script>

<template>
  <nav class="navbar" role="navigation" aria-label="main navigation">
    <div class="navbar-brand">
      <router-link to="/" class="navbar-item">
        <img src="../assets/favicon.png">
      </router-link>
    
      <a role="button" class="navbar-burger" aria-label="menu" aria-expanded="false" data-target="navbarBasicExample" @click="toggleMobileMenu">
        <span aria-hidden="true"></span>
        <span aria-hidden="true"></span>
        <span aria-hidden="true"></span>
      </a>
    </div>
  
    <div id="navbarBasicExample" class="navbar-menu" :class="{'is-active': showMobileMenu}">
      <div class="navbar-start">
        <router-link to="/" class="navbar-item">Home</router-link>
        
  
        <a class="navbar-item">
          Documentation
        </a>
  
        <div class="navbar-item has-dropdown is-hoverable">
          <a class="navbar-link">
            More
          </a>
  
          <div class="navbar-dropdown">
            <a class="navbar-item">
              About
            </a>
            <a class="navbar-item">
              Contact
            </a>
            <hr class="navbar-divider">
            <a class="navbar-item">
              Report an issue
            </a>
          </div>
        </div>
      </div>
  
      <div class="navbar-end">
        <div class="navbar-item">
          <div v-if="$store.state.isAuthenticated" class="buttons">
            <router-link to="/sign-up" class="button is-info"><strong>My Account</strong></router-link>
            <button class="button is-light" @click="logout"><strong>Log out</strong></button>
          </div>
          <div v-else class="buttons">
            <router-link to="/sign-up" class="button is-info"><strong>Sign up</strong></router-link>
            <router-link to="/log-in" class="button is-light"><strong>Log in</strong></router-link>
          </div>
        </div>
      </div>
    </div>
  </nav>
</template>

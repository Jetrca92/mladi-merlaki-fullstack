<template>

    <div v-if="$store.state.isAuthenticated">
        <section>

        </section>
    </div>

    <div v-else>
        <LandingPage />
    </div>
</template>

<script setup>
import LandingPage from '../components/LandingPage.vue'
</script>

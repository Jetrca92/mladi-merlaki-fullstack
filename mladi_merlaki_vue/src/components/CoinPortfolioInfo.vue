<template>
    <h3 class="title is-3">Your shares</h3>
    <h1 class="title is-1 mb-3">${{ Number(valueOfShares(coin, store)).toLocaleString() }}</h1>
    <p><strong>Number of shares: </strong> {{ sharesInPortfolio(coin, store).toLocaleString() }}</p>
    <p class="mb-3"><strong>Avg price: </strong> {{ averageBuyPrice(coin, store).toLocaleString() }}</p>
</template>

<script setup>
import { useStore } from 'vuex'
import { sharesInPortfolio, valueOfShares, averageBuyPrice } from './helpers.js'

const store = useStore()
const props = defineProps(['coin'])
</script>
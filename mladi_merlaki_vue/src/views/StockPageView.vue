<template>
    <section class="section">
        <div class="box">
            <h3 class="title is-3">{{ stock.name }} ({{ stock.symbol }})</h3>
            <h1 class="title is-1 mb-3">${{ stock.price}}</h1>
            <div class="content">
                <p><strong>Market Cap:</strong> ${{ stock.market_cap}}</p>
                <p><strong>24 Hour Trading Volume:</strong> ${{ stock.volume}}</p>
                <p><strong>Dividend:</strong> ${{ stock.dividend}}</p>
            </div>
        </div>

    </section>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import axios from 'axios'

const stock = ref({})
const route = useRoute()
const getStock = () => {
    const stockId = route.params.id
    axios.get(`api/v1/marketdata/stocks/${stockId}/`)
        .then(response => {
        stock.value = response.data
        })
        .catch(error => {
        console.error(error)
        })
}
getStock()
</script>
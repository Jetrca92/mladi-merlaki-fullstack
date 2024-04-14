<template>
    <h3 class="title is-3">{{ stock.name }} ({{ stock.symbol }})</h3>
    <h1 class="title is-1 mb-3">${{ Number(stock.price).toLocaleString() }}</h1>
    <div class="content">
        <p><strong>Country: </strong> {{ stock.country }}</p>
        <p><strong>Sector:</strong> {{ stock.sector }}</p>
        <p><strong>Market Cap:</strong> ${{ Number(stock.market_cap).toLocaleString() }}</p>
        <p><strong>24 Hour Trading Volume:</strong> ${{ Number(stock.volume).toLocaleString() }}</p>
        <p><strong>Dividend:</strong> ${{ Number(stock.dividend).toLocaleString() }}</p>
    </div>
</template>

<script setup>
const { props } = defineProps(['stock'])
</script>
<template>
    <h3 class="title is-3">
        <img :src="props.coin.logo" style="width: 25px; height: auto; margin-right: 5px;" class="mr-3">
        {{ props.coin.name }} ({{ props.coin.symbol }})</h3>
    <h1 class="title is-1 mb-3">${{ Number(props.coin.price).toLocaleString() }}</h1>
    <div class="content">
        <p><strong>Market Cap:</strong> ${{ Number(props.coin.market_cap).toLocaleString() }}</p>
        <p><strong>24 Hour Trading Volume:</strong> ${{ Number(props.coin.volume).toLocaleString() }}</p>
    </div>
</template>

<script setup>
const props = defineProps(['coin'])
</script>
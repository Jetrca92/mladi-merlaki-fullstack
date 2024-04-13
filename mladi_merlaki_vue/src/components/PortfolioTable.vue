<script setup>
import { ref } from 'vue'
import { useStore } from 'vuex'

const store = useStore()
store.dispatch('fetchPortfolio')
const portfolio = ref(store.state.portfolio)

const calculateTotal = () => {
    if (!portfolio.value.stocks || !portfolio.value.crypto) {
        return 0;
    }
    let total = portfolio.value.cash;
    for (const stock of portfolio.value.stocks) {
        total += stock.shares * stock.stock.price;
    }
    for (const coin of portfolio.value.crypto) {
        total += coin.shares * coin.coin.price;
    }
    return total;
}

</script>

<template>
    <table class="table is-fullwidth">
    <thead>
        <tr>
            <th colspan="4" class="has-text-centered"><h3>Stocks and ETFs</h3></th>
        </tr>
        <tr>
            <th>Name</th>
            <th class="has-text-right">Shares</th>
            <th class="has-text-right">Price</th>
            <th class="has-text-right">TOTAL</th>
        </tr>
    </thead>
    <tbody>
        <tr v-for="asset in portfolio.stocks" :key="asset.id">
            <td>{{ asset.stock.name }} ({{ asset.stock.symbol }})</td>
            <td class="has-text-right">{{ Number(asset.shares).toLocaleString() }}</td>
            <td class="has-text-right">{{ Number(asset.stock.price).toLocaleString() }} $</td>
            <td class="has-text-right">{{ Number(asset.shares * asset.stock.price).toLocaleString() }} $</td>
        </tr>
    </tbody>
    <thead>
        <tr>
            <th colspan="4" class="has-text-centered"><h3>Crypto</h3></th>
        </tr>
        <tr>
            <th>Name</th>
            <th class="has-text-right">Shares</th>
            <th class="has-text-right">Price</th>
            <th class="has-text-right">TOTAL</th>
        </tr>
    </thead>
    <tbody>
        <tr v-for="asset in portfolio.crypto" :key="asset.id">
            <td>{{ asset.coin.name }} ({{ asset.coin.symbol }})</td>
            <td class="has-text-right">{{ Number(asset.shares).toLocaleString() }}</td>
            <td class="has-text-right">{{ Number(asset.coin.price).toLocaleString() }} $</td>
            <td class="has-text-right">{{ Number(asset.shares * asset.coin.price).toLocaleString() }} $</td>
        </tr>
    </tbody>
    <tfoot>
        <tr>
            <td colspan="4"></td>
        </tr>
        <tr>
            <td colspan="3" class="has-text-right is-uppercase has-text-weight-bold">Cash</td>
            <td class="has-text-right">{{ Number(portfolio.cash).toLocaleString() }} $</td>
        </tr>
        <tr>
            <td colspan="3" class="has-text-right is-uppercase has-text-weight-bold">TOTAL</td>
            <td class="has-text-right">{{ calculateTotal().toLocaleString() }} $</td>
        </tr>
    </tfoot>
</table>
</template>

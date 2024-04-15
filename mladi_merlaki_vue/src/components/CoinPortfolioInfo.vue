<template>
    <h3 class="title is-3">Your shares</h3>
    <h1 class="title is-1 mb-3">${{ Number(valueOfShares(coin)).toLocaleString() }}</h1>
    <p><strong>Number of shares: </strong> {{ sharesInPortfolio(coin).toLocaleString() }}</p>
    <p class="mb-3"><strong>Avg price: </strong> {{ averagePrice(coin).toLocaleString() }}</p>
</template>

<script setup>
import { useStore } from 'vuex'

const store = useStore()
const props = defineProps(['coin'])
const sharesInPortfolio = (coin) => {
    const portfolio = store.state.portfolio;
    const cryptoPortfolio = portfolio.crypto.find(cryptoPortfolio => cryptoPortfolio.coin.symbol === coin.symbol)
    return cryptoPortfolio ? cryptoPortfolio.shares : 0
}

const valueOfShares = (coin) => {
    const portfolio = store.state.portfolio;
    const cryptoPortfolio = portfolio.crypto.find(cryptoPortfolio => cryptoPortfolio.coin.symbol === coin.symbol)
    return cryptoPortfolio ? cryptoPortfolio.shares * cryptoPortfolio.coin.price : 0
}

const averagePrice = (coin) => {
    const transactions = store.state.portfolio.transactions
    if (!transactions || transactions.length === 0) {
        return null; // Return null if transactions is null or empty
    }
    const symbolTransactions = transactions.filter(transaction => transaction.symbol === coin.symbol)
    if (symbolTransactions.length === 0) {
        return null; // Return null if there are no transactions for the symbol
    }
    const totalAmount = symbolTransactions.reduce((acc, transaction) => acc + (transaction.shares * transaction.price), 0)
    const totalShares = symbolTransactions.reduce((acc, transaction) => acc + transaction.shares, 0)
    return totalAmount / totalShares
}
</script>
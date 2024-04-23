<template>
    <h3 class="title is-3">Your shares</h3>
    <h1 class="title is-1 mb-3">${{ Number(valueOfShares(stock)).toLocaleString() }}</h1>
    <p><strong>Number of shares: </strong> {{ sharesInPortfolio(stock) }}</p>
    <p class="mb-3"><strong>Avg price: </strong> {{ averagePrice(stock) }}</p>
</template>

<script setup>
import { useStore } from 'vuex'

const store = useStore()
const props = defineProps(['stock'])
const sharesInPortfolio = (stock) => {
    const portfolio = store.state.portfolio;
    const stockPortfolio = portfolio.stocks.find(stockPortfolio => stockPortfolio.stock.symbol === stock.symbol)
    return stockPortfolio ? stockPortfolio.shares : 0
}

const valueOfShares = (stock) => {
    const portfolio = store.state.portfolio;
    const stockPortfolio = portfolio.stocks.find(stockPortfolio => stockPortfolio.stock.symbol === stock.symbol)
    return stockPortfolio ? stockPortfolio.shares * stockPortfolio.stock.price : 0
}

const averagePrice = (stock) => {
    const transactions = store.state.portfolio.transactions
    console.log(transactions)
    if (!transactions || transactions.length === 0) {
        return null; // Return null if transactions is null or empty
    }
    const symbolTransactions = transactions.filter(transaction => transaction.symbol === stock.symbol && transaction.type === 'buy')
    if (symbolTransactions.length === 0) {
        return null; // Return null if there are no transactions for the symbol
    }
    const totalAmount = symbolTransactions.reduce((acc, transaction) => acc + (transaction.shares * transaction.price), 0)
    const totalShares = symbolTransactions.reduce((acc, transaction) => acc + transaction.shares, 0)
    return totalAmount / totalShares
}
</script>
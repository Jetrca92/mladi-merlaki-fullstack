<template>
    <section class="section">
        <div class="box">
            <div class="columns">
            
                <!-- stock info and buy option -->
                <div class="column">
                    <h3 class="title is-3">{{ stock.name }} ({{ stock.symbol }})</h3>
                    <h1 class="title is-1 mb-3">${{ Number(stock.price).toLocaleString() }}</h1>
                    <div class="content">
                        <p><strong>Country: </strong> {{ stock.country }}</p>
                        <p><strong>Sector:</strong> {{ stock.sector }}</p>
                        <p><strong>Market Cap:</strong> ${{ Number(stock.market_cap).toLocaleString() }}</p>
                        <p><strong>24 Hour Trading Volume:</strong> ${{ Number(stock.volume).toLocaleString() }}</p>
                        <p><strong>Dividend:</strong> ${{ Number(stock.dividend).toLocaleString() }}</p>

                    </div>

                    <form @submit.prevent="submitBuyForm" class="mb-3" v-if="store.state.isAuthenticated"> 
                        <div class="field has-addons">
                            <div class="control">
                                <input autocomplete="off" class="input" id="shares" name="shares" placeholder="Shares" type="number" min="1" step="1" v-model="shares">
                            </div>
                            <div class="control">
                                <button class="button is-info">Buy</button>
                            </div>
                        </div>
                    </form>

                    <p v-if="shares && shares > 0 && stock.price && (shares * stock.price) <= store.state.portfolio.cash" class="is-size-6 is-italic">Total: ${{ (shares * stock.price).toLocaleString() }}</p>
                    <p v-if="shares && shares > 0 && stock.price && (shares * stock.price) >= store.state.portfolio.cash" class="is-danger is-size-6 is-italic">Not enough cash in portfolio.</p>
                    
                    <article v-if="successMessageVisible" class="message is-primary my-5">
                        <div class="message-header">
                            <p>Success!</p>
                            <button @click="hideSuccessMessage" class="delete" aria-label="delete"></button>
                        </div>
                        <div class="message-body">
                            You've successfully purchased {{ shares }} shares of {{ stock.symbol }} for ${{ t }}.
                        </div>
                    </article>

                    <article v-if="errorMessageVisible" class="message is-danger my-5">
                        <div class="message-header">
                            <p>Failed to submit!</p>
                            <button @click="hideErrorMessage" class="delete" aria-label="delete"></button>
                        </div>
                        <div class="message-body">
                            {{ errorMessageContent }}
                        </div>
                    </article>

                </div>

                <!-- sell option if user has stock in portfolio -->
                <div v-if="stockInPortfolio(stock)" class="column">
                    <h3 class="title is-3">Your shares</h3>
                    <h1 class="title is-1 mb-3">${{ Number(valueOfShares(stock)).toLocaleString() }}</h1>
                    <p><strong>Number of shares: </strong> {{ sharesInPortfolio(stock) }}</p>
                    <p class="mb-3"><strong>Avg price: </strong> {{ averagePrice(stock) }}</p>

                    <form @submit.prevent="submitSellForm" class="mb-3" v-if="store.state.isAuthenticated"> 
                        <div class="field has-addons">
                            <div class="control">
                                <input autocomplete="off" class="input" id="sell_shares" name="sell_shares" placeholder="Shares" type="number" min="1" step="1" v-model="sell_shares">
                            </div>
                            <div class="control">
                                <button class="button is-danger">Sell</button>
                            </div>
                        </div>
                    </form>

                </div>
      
            </div>
        </div>
    </section>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { useStore } from 'vuex'
import axios from 'axios'

const stock = ref({})
const shares = ref()
const sell_shares = ref()
const successMessageVisible = ref(false)
const errorMessageVisible = ref(false)
const errorMessageContent = ref('')
const t = ref()
const store = useStore()
const route = useRoute()

const total = () => {
    t.value = stock.value.price * shares.value
}

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
onMounted(getStock)

const submitBuyForm = async () => {
    if (!shares.value || shares.value <= 0) {
        console.error("Invalid number of shares");
        return
    }
    if (shares.value * stock.value.price > store.state.portfolio.cash) {
        errorMessageContent.value = 'Not enough cash in portfolio!'
        errorMessageVisible.value = true 
        return
    }
    const formData = {
        stock: stock.value,
        shares: shares.value,
    }
    const csrftoken = getCookie("csrftoken")
    const config = {
        headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": csrftoken
        }
    }
    await axios
        .post("/api/v1/portfolio/buy_stock/", formData, config)
        .then(response => {
            successMessageVisible.value = true 
            total()
            store.dispatch('fetchPortfolio')
        })
        .catch(error => {
        console.error(error)
        })
}

const submitSellForm = async () => {
    if (!shares.value || shares.value <= 0) {
        console.error("Invalid number of shares");
        return
    }
    if (shares.value * stock.value.price > store.state.portfolio.cash) {
        errorMessageContent.value = 'Not enough cash in portfolio!'
        errorMessageVisible.value = true 
        return
    }
    const formData = {
        stock: stock.value,
        shares: sell_shares.value,
    }
    const csrftoken = getCookie("csrftoken")
    const config = {
        headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": csrftoken
        }
    }
    await axios
        .post("/api/v1/portfolio/buy_stock/", formData, config)
        .then(response => {
            successMessageVisible.value = true 
            total()
            store.dispatch('fetchPortfolio')
        })
        .catch(error => {
        console.error(error)
        })
}

const hideSuccessMessage = () => {
    successMessageVisible.value = false
}

const hideErrorMessage = () => {
    errorMessageVisible.value = false
}

const getCookie = (name) => {
    let cookieValue = null;
    if (document.cookie && document.cookie !== "") {
        const cookies = document.cookie.split(";");
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === name + "=") {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

const stockInPortfolio = (stock) => {
    const portfolio = store.state.portfolio
    if (portfolio && portfolio.stocks) {
        return portfolio.stocks.some(stockPortfolio => stockPortfolio.stock.symbol === stock.symbol)
    }
    return false;
}

const sharesInPortfolio = (stock) => {
    const portfolio = store.state.portfolio;
    const stockPortfolio = portfolio.stocks.find(stockPortfolio => stockPortfolio.stock.symbol === stock.symbol);
    return stockPortfolio ? stockPortfolio.shares : 0;
}

const valueOfShares = (stock) => {
    const portfolio = store.state.portfolio;
    const stockPortfolio = portfolio.stocks.find(stockPortfolio => stockPortfolio.stock.symbol === stock.symbol);
    return stockPortfolio ? stockPortfolio.shares * stockPortfolio.stock.price : 0;
}

const averagePrice = (stock) => {
    const transactions = store.state.portfolio.transactions;
    if (!transactions || transactions.length === 0) {
        return null; // Return null if transactions is null or empty
    }
    const symbolTransactions = transactions.filter(transaction => transaction.symbol === stock.symbol);
    if (symbolTransactions.length === 0) {
        return null; // Return null if there are no transactions for the symbol
    }
    const totalAmount = symbolTransactions.reduce((acc, transaction) => acc + (transaction.shares * transaction.price), 0);
    const totalShares = symbolTransactions.reduce((acc, transaction) => acc + transaction.shares, 0);
    return totalAmount / totalShares;
};
</script>
<template>
    <section class="section">
        <div class="box">
            <div class="columns">
            
                <!-- stock info and buy option -->
                <div class="column">
                    <StockInfo :stock="stock" />
                    <BuyStockForm :stock="stock" :getCookie="getCookie" />
                    
                    

                </div>

                <!-- sell option if user has stock in portfolio -->
                <div v-if="stockInPortfolio(stock)" class="column">
                    <StockPortfolioInfo :stock="stock" />
                    <SellStockForm :stock="stock" :getCookie="getCookie" />
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

import StockInfo from "../components/StockInfo.vue"
import BuyStockForm from "../components/BuyStockForm.vue"
import StockPortfolioInfo from "../components/StockPortfolioInfo.vue"
import SellStockForm from "../components/SellStockForm.vue"

const stock = ref({})
const store = useStore()
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
onMounted(getStock)

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
</script>

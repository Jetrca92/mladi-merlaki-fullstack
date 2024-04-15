<template>
    <section class="section">
        <div class="box">
            <div class="columns">

                <!-- coin info and buy option -->
                <div class="column">
                    <CoinInfo :coin="coin" />
                    <BuyCryptoForm :coin="coin" :getCookie="getCookie" />
                </div>

                <!-- sell option if user has stock in portfolio -->
                <div v-if="coinInPortfolio(coin)" class="column">
                    <CoinPortfolioInfo :coin="coin" />
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

import BuyCryptoForm from '../components/BuyCryptoForm.vue'
import CoinInfo from '../components/CoinInfo.vue'
import CoinPortfolioInfo from '../components/CoinPortfolioInfo.vue'

const coin = ref({})
const route = useRoute()
const store = useStore()

const getCoin = () => {
    const coinId = route.params.id
    axios.get(`api/v1/marketdata/crypto/${coinId}/`)
        .then(response => {
        coin.value = response.data
        })
        .catch(error => {
        console.error(error)
        })
}
onMounted(getCoin)

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

const coinInPortfolio = (coin) => {
    const portfolio = store.state.portfolio
    if (portfolio && portfolio.crypto) {
        return portfolio.crypto.some(cryptoPortfolio => cryptoPortfolio.coin.symbol === coin.symbol)
    }
    return false;
}
</script>

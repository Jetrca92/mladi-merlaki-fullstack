<template>
    <section class="section">
        <div class="box">
            <h3 class="title is-3">{{ stock.name }} ({{ stock.symbol }})</h3>
            <h1 class="title is-1 mb-3">${{ stock.price}}</h1>
            <div class="content">
                <p><strong>Country: </strong> {{ stock.country }}</p>
                <p><strong>Sector:</strong> {{ stock.sector }}</p>
                <p><strong>Market Cap:</strong> ${{ stock.market_cap}}</p>
                <p><strong>24 Hour Trading Volume:</strong> ${{ stock.volume}}</p>
                <p><strong>Dividend:</strong> ${{ stock.dividend}}</p>

            </div>

            <form @submit.prevent="submitForm">
                <div class="field has-addons">
                    <div class="control">
                        <input autocomplete="off" class="input" id="shares" name="shares" placeholder="Shares" type="number" min="1" step="1" v-model="shares">
                    </div>
                    <div class="control">
                        <button class="button is-primary">Buy</button>
                    </div>
                </div>
            </form>

        </div>

    </section>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import axios from 'axios'

const stock = ref({})
const shares = ref()
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

const submitForm = async () => {
    if (!shares.value || shares.value <= 0) {
        console.error("Invalid number of shares");
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
            shares.value = '' 
        })
        .catch(error => {
        console.error(error)
        })
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


</script>
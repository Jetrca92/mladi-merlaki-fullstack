<template>
    <section class="section">
        <div class="box">
            <h3 class="title is-3"><img :src="coin.logo" style="width: 25px; height: auto; margin-right: 5px;" class="mr-3">{{ coin.name }} ({{ coin.symbol }})</h3>
            <h1 class="title is-1 mb-3">${{ coin.price}}</h1>
            <div class="content">
                <p><strong>Market Cap:</strong> ${{ coin.market_cap}}</p>
                <p><strong>24 Hour Trading Volume:</strong> ${{ coin.volume}}</p>
            </div>

            <form @submit.prevent="submitForm" class="mb-3" v-if="$store.state.isAuthenticated">
                <div class="field has-addons">
                    <div class="control">
                        <input autocomplete="off" class="input" id="shares" name="shares" placeholder="Shares" type="number" min="1" step="1" v-model="shares">
                    </div>
                    <div class="control">
                        <button class="button is-info">Buy</button>
                    </div>
                </div>
            </form>

            <article v-if="successMessageVisible" class="message is-primary my-5">
                <div class="message-header">
                    <p>Success!</p>
                    <button @click="hideSuccessMessage" class="delete" aria-label="delete"></button>
                </div>
                <div class="message-body">
                    You've successfully purchased {{ shares }} shares of {{ coin.symbol }} for ${{ t }}.
                </div>
            </article>
        </div>

    </section>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import axios from 'axios'

const coin = ref({})
const shares = ref()
const successMessageVisible = ref(false)
const t = ref()
const total = () => {
    t.value = coin.value.price * shares.value
}
const route = useRoute()

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

const submitForm = async () => {
    if (!shares.value || shares.value <= 0) {
        console.error("Invalid number of shares");
        return
    }
    const formData = {
        coin: coin.value,
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
        .post("/api/v1/portfolio/buy_crypto/", formData, config)
        .then(response => {
            successMessageVisible.value = true 
            total()
        })
        .catch(error => {
        console.error(error)
        })
}

const hideSuccessMessage = () => {
    successMessageVisible.value = false
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
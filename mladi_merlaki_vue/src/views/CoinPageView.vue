<template>
    <section class="section">
        <div class="box">
            <CoinInfo :coin="coin" />
            <BuyCryptoForm :coin="coin" :getCookie="getCookie" />

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

import BuyCryptoForm from '../components/BuyCryptoForm.vue'
import CoinInfo from '../components/CoinInfo.vue'

const coin = ref({})
const successMessageVisible = ref(false)
const t = ref()
const route = useRoute()

const total = () => {
    t.value = coin.value.price * shares.value
}

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
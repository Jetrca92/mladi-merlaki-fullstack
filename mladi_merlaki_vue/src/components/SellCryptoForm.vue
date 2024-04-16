<template>
    <form @submit.prevent="submitSellForm" class="mb-3" v-if="store.state.isAuthenticated"> 
        <div class="field has-addons">
            <div class="control">
                <input autocomplete="off" class="input" id="shares" name="shares" placeholder="Shares" type="number" min="0.01" step="0.01" v-model="shares">
            </div>
            <div class="control">
                <button class="button is-danger">Sell</button>
            </div>
        </div>
    </form>

    <p 
        v-if="shares && shares > 0 && props.coin.price && shares <= sharesInPortfolio(props.coin)" 
        class="is-size-6 is-italic"
    >
        Total: ${{ (shares * props.coin.price).toLocaleString() }}
    </p>
    <p 
        v-if="shares && shares > sharesInPortfolio(props.coin)" 
        class="is-danger is-size-6 is-italic"
    >
        Not enough shares in portfolio.
    </p>

    <article v-if="successMessageVisible" class="message is-primary my-5">
        <div class="message-header">
            <p>Success!</p>
            <button @click="hideSuccessMessage" class="delete" aria-label="delete"></button>
        </div>
        <div class="message-body">
            You've successfully sold {{ shares }} shares of {{ props.coin.symbol }} for ${{ t }}.
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
</template>

<script setup>
import { ref } from 'vue'
import { useStore } from 'vuex'
import axios from 'axios'

const t = ref()
const successMessageVisible = ref(false)
const errorMessageVisible = ref(false)
const errorMessageContent = ref('')
const store = useStore()
const shares = ref()
const props = defineProps({
    coin: {
        type: Object,
        required: true
    },
    getCookie: {
        type: Function,
        required: true
    },
})

const submitSellForm = async () => {
    if (!shares.value || shares.value <= 0) {
        errorMessageContent.value = 'Invalid number of shares!'
        errorMessageVisible.value = true
        return
    }
    if (shares.value > sharesInPortfolio(props.coin)) {
        errorMessageContent.value = 'Not enough shares in portfolio!'
        errorMessageVisible.value = true 
        return
    }
    const formData = {
        coin: props.coin,
        shares: shares.value,
    }
    const csrftoken = props.getCookie("csrftoken")
    const config = {
        headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": csrftoken
        }
    }
    await axios
        .post("/api/v1/portfolio/sell_crypto/", formData, config)
        .then(response => {
            successMessageVisible.value = true 
            total()
            store.dispatch('fetchPortfolio')
        })
        .catch(error => {
        console.error(error)
        })
}

const sharesInPortfolio = (coin) => {
    const portfolio = store.state.portfolio;
    const cryptoPortfolio = portfolio.crypto.find(cryptoPortfolio => cryptoPortfolio.coin.symbol === coin.symbol)
    return cryptoPortfolio ? cryptoPortfolio.shares : 0
}

const hideSuccessMessage = () => {
    successMessageVisible.value = false
}

const hideErrorMessage = () => {
    errorMessageVisible.value = false
}

const total = () => {
    t.value = props.coin.price * shares.value
}

</script>

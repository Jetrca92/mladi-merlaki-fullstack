<template>
    <form @submit.prevent="submitForm" class="mb-3" v-if="$store.state.isAuthenticated">
        <div class="field has-addons">
            <div class="control">
                <input autocomplete="off" class="input" id="shares" name="shares" placeholder="Shares" type="number" min="0.01" step="0.01" v-model="shares">
            </div>
            <div class="control">
                <button class="button is-info">Buy</button>
            </div>
        </div>
    </form>

    <p 
        v-if="shares && shares > 0 && props.coin.price && (shares * props.coin.price) <= store.state.portfolio.cash" 
        class="is-size-6 is-italic"
    >
        Total: ${{ (shares * props.coin.price).toLocaleString() }}
    </p>
    <p 
        v-if="shares && shares > 0 && props.coin.price && (shares * props.coin.price) >= store.state.portfolio.cash" 
        class="is-danger is-size-6 is-italic"
    >
        Not enough cash in portfolio.
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
const shares = ref()
const store = useStore()
const successMessageVisible = ref(false)
const errorMessageVisible = ref(false)
const errorMessageContent = ref('')

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

const submitForm = async () => {
    if (!shares.value || shares.value <= 0) {
        errorMessageContent.value = 'Invalid number of shares!'
        errorMessageVisible.value = true
        return
    }
    if (shares.value * props.coin.price > store.state.portfolio.cash) {
        errorMessageContent.value = 'Not enough cash in portfolio!'
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
        .post("/api/v1/portfolio/buy_crypto/", formData, config)
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

const total = () => {
    t.value = props.coin.price * shares.value
}
</script>
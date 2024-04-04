<template>
    <section class="section">

        <table class="table is-hoverable is-fullwidth" id="rankings-table">
            <thead>
                <tr>
                    <th scope="col">#</th>
                    <th class="text-start" scope="col">Username</th>
                    <th class="text-start" scope="col">Stocks</th>
                    <th class="text-start" scope="col">Crypto</th>
                    <th class="text-start" scope="col">Cash</th>
                    <th class="text-start" scope="col">Total</th>
                </tr>
            </thead>
            <tbody>
                <tr v-for="(data, index) in rankings" :key="data.id">
                    <th scope="row">{{ index + 1 }}</th>
                    <td class="text-start">{{ data.username }}</td>
                    <td class="text-start">${{ Number(data.stocks_total).toLocaleString() }}</td>
                    <td class="text-start">${{ Number(data.crypto_total).toLocaleString() }}</td>
                    <td class="text-start">${{ Number(data.cash).toLocaleString() }}</td>
                    <td class="text-start">${{ Number(data.total).toLocaleString() }}</td>
                </tr>
            </tbody>
        </table>

    </section>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'

const rankings = ref([])

const getRankings = () => {
    axios.get(`api/v1/portfolio/rankings/`)
        .then(response => {
            rankings.value = response.data 
        })
        .catch(error => {
        console.error(error)
        })
}
onMounted(getRankings)

</script>
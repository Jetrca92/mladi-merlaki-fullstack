<template>
    <section class="section">
        <table class="table is-striped is-fullwidth">
            <thead>
                <tr>
                    <th>Symbol</th>
                    <th>Asset class</th>
                    <th>Type</th>
                    <th class="has-text-right">Shares</th>
                    <th class="has-text-right">Price</th>
                    <th class="has-text-right">Transacted</th>
                </tr>
            </thead>
            <tbody>
                <tr v-for="transaction in transactions" :key="transaction.id">
                    <td>{{ transaction.symbol }}</td>
                    <td>{{ transaction.asset_class }}</td>
                    <td>{{ transaction.type }}</td>
                    <td class="has-text-right">{{ transaction.shares }}</td>
                    <td class="has-text-right">{{ transaction.price}}</td>
                    <td class="has-text-right">{{ formatDate(transaction.date) }}</td>
                </tr>
            </tbody>
        </table>
    </section>

</template>

<script setup>
import { ref, onMounted } from 'vue'
import { format } from 'date-fns'
import axios from 'axios'

const transactions = ref([])

const getTransactions = () => {
    axios.get(`api/v1/portfolio/transactions/`)
        .then(response => {
            transactions.value = response.data 
        })
        .catch(error => {
        console.error(error)
        })
}
onMounted(getTransactions)

const formatDate = (dateTimeString) => {
    return format(new Date(dateTimeString), 'dd/MM/yyyy - HH:mm:ss');
}
</script>
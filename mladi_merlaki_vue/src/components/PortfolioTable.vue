<script setup>
import axios from 'axios'
import { ref } from 'vue'
import { useStore } from 'vuex'
import { useRouter } from 'vue-router'

const portfolio = {}

</script>

<template>
    <table class="table is-fullwidth">
    <thead>
        <tr>
            <th colspan="4" class="has-text-centered"><h3>Stocks and ETFs</h3></th>
        </tr>
        <tr>
            <th>Name</th>
            <th class="has-text-right">Shares</th>
            <th class="has-text-right">Price</th>
            <th class="has-text-right">TOTAL</th>
        </tr>
    </thead>
    <tbody>
        <tr v-for="asset in portfolio">
            <td>{{ asset.stock.name }} ({{ asset.stock.symbol }})</td>
            <td class="has-text-right">{{ asset.shares }}</td>
            <td class="has-text-right">{{ asset.stock.price }}</td>
            <td class="has-text-right">total</td>
        </tr>
    </tbody>
    <thead>
        <tr>
            <th colspan="4" class="has-text-centered"><h3>Crypto</h3></th>
        </tr>
        <tr>
            <th>Name</th>
            <th class="has-text-right">Shares</th>
            <th class="has-text-right">Price</th>
            <th class="has-text-right">TOTAL</th>
        </tr>
    </thead>
    <tbody>
        <tr v-for="asset in portfolio">
            <td>{{ asset.coin.name }} ({{ asset.coin.symbol|up }})</td>
            <td class="has-text-right">{{ asset.shares }}</td>
            <td class="has-text-right">{{ asset.coin.price }}</td>
            <td class="has-text-right">{{ asset.shares }}</td>
        </tr>
    </tbody>
    <tfoot>
        <tr>
            <td colspan="4"></td>
        </tr>
        <tr>
            <td colspan="3" class="has-text-right is-uppercase has-text-weight-bold">Cash</td>
            <td class="has-text-right">{{ portfolio.cash }}</td>
        </tr>
        <tr>
            <td colspan="3" class="has-text-right is-uppercase has-text-weight-bold">TOTAL</td>
            <td class="has-text-right">{{ total }}</td>
        </tr>
    </tfoot>
</table>
</template>

<template>
    <section class="section">
        
        <div class="columns is-variable is-1">
            <div class="column is-half">
                <form class="is-inline" @submit.prevent="search">
                    <div class="field">
                        <label for="search" class="label">Search:</label>
                        <div class="control">
                            <div class="">
                                <div class="is-half">
                                    <input class="input" style="width: 50%;" type="text" placeholder="Company name" id="search" name="name" @keyup="delayedSearch" />
                                </div>
                                
                            </div>
                        </div>
                    </div>
                </form>
            </div>
            
            <div class="column is-half has-text-right">
                <form class="is-inline" @submit.prevent="sortBy">
                    <div class="field">
                        <label for="sort" class="label">Sort by:</label>
                        <div class="control">
                            <div class="select">
                                <select name="sort" id="sort" v-model="selectedSort">
                                    <option value="-market_cap">Market cap descending</option>
                                    <option value="market_cap">Market cap ascending</option>
                                    <option value="-volume">Volume descending</option>
                                    <option value="volume">Volume ascending</option>
                                </select>
                            </div>
                        </div>
                    </div>
                </form>
            </div>

        </div>
        

        <div>
            <table class="table is-fullwidth is-hoverable" id="stocks-table" v-if="stocks.length > 0">
                <thead>
                    <tr>
                        <th class="is-info">#</th>
                        <th class="is-info">Stock</th>
                        <th class="is-info">Price</th>
                        <th class="is-info">Sector</th>
                        <th class="is-info">Volume</th>
                        <th class="is-info">Market Cap</th>
                        <th class="is-info">Country</th>
                    </tr>
                </thead>
                <tbody>
                    <tr v-for="(stock, index) in stocks" :key="stock.id">
                        <th scope="row">{{ index + 1 }}</th>
                        <td><a href="" class="navbar-item">{{ stock.name }} ({{ stock.symbol }})</a></td>
                        <td>{{ stock.price}}</td>
                        <td>{{ stock.sector }}</td>
                        <td>{{ stock.volume}}</td>
                        <td>{{ stock.market_cap}}</td>
                        <td>{{ stock.country }}</td>
                    </tr>
                </tbody>
            </table>
            <div v-else>
                No stocks found.
            </div>
        </div>
    </section>
    
</template>


<script setup>
import { ref } from 'vue'
import axios from 'axios'
const stocks = ref({})
const getPortfolio = () => {
    axios.get(`api/v1/marketdata/stocks/`)
        .then(response => {
        stocks.value = response.data
        
        })
        .catch(error => {
        console.error(error)
        })
}
getPortfolio()
</script>

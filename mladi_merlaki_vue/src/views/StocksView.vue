<template>
    <section class="section">
        <div class="mb-3">

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
                        <td>{{ stock.price | usd }}</td>
                        <td>{{ stock.sector }}</td>
                        <td>{{ stock.volume | usd }}</td>
                        <td>{{ stock.market_cap | usd }}</td>
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
const stocks = ref([
        { id: 1, name: 'Stock A', symbol: 'STK-A', price: 100.50, sector: 'Technology', volume: 100000, market_cap: 5000000, country: 'USA' },
        { id: 2, name: 'Stock B', symbol: 'STK-B', price: 75.25, sector: 'Financial Services', volume: 80000, market_cap: 4000000, country: 'UK' }
    ])
</script>

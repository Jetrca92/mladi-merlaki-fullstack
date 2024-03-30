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
                                    <input class="input" style="width: 50%;" type="text" placeholder="Company name" id="search" name="name" v-model="filterInput" />
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
                                <select name="sort" id="sort" v-model="selectedSort" @change="sortBy">
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
                    <tr v-for="(stock, index) in pagedStocks" :key="stock.id">
                        <th scope="row">{{ (currentPage - 1) * itemsPerPage + index + 1 }}</th>
                        <td><a :href="`/stocks/${stock.id}`" class="navbar-item">{{ stock.name }} ({{ stock.symbol }})</a></td>
                        <td>${{ stock.price}}</td>
                        <td>{{ stock.sector }}</td>
                        <td>${{ stock.volume}}</td>
                        <td>${{ stock.market_cap}}</td>
                        <td>{{ stock.country }}</td>
                    </tr>
                </tbody>
            </table>
            <div v-else>
                No stocks found.
            </div>
            <nav class="pagination is-centered" role="navigation" aria-label="pagination">
                <ul class="pagination-list">
                    <li>
                        <button class="pagination-previous" :disabled="currentPage === 1" @click="goToPage(currentPage - 1)">Previous</button>
                    </li>
                    <li v-for="pageNumber in totalPages" :key="pageNumber">
                        <button class="pagination-link" :class="{ 'is-current': pageNumber === currentPage }" @click="goToPage(pageNumber)">{{ pageNumber }}</button>
                    </li>
                
                    <li>
                        <button class="pagination-next" :disabled="currentPage === totalPages" @click="goToPage(currentPage + 1)">Next</button>
                    </li>
                </ul>
            </nav>
        </div>
    </section>
    
</template>


<script setup>
import { ref, computed, onMounted } from 'vue'
import axios from 'axios'

const stocks = ref([])
const selectedSort = ref('-market_cap')
const filterInput = ref('')
const itemsPerPage = 100
let currentPage = ref(1)

// Get stock data from API
const getStocksData = () => {
    axios.get(`api/v1/marketdata/stocks/`)
        .then(response => {
        stocks.value = response.data
        })
        .catch(error => {
        console.error(error)
        })
}
onMounted(getStocksData)

// Filter and sort stocks
const sortedStocks = computed(() => {
    const copiedStocks = [...stocks.value]
    copiedStocks.sort((a, b) => {
        // Compare the values based on the selected sorting criteria
        if (a[selectedSort.value] < b[selectedSort.value]) {
            return -1
        } else if (a[selectedSort.value] > b[selectedSort.value]) {
            return 1
        } else {
            return 0
        }
    })
    if(filterInput.value !== "") {
        return copiedStocks.filter(stock => stock.name.toLowerCase().includes(filterInput.value.toLowerCase()));
    } 
    return copiedStocks
})

// Pagination
const pagedStocks = computed(() => {
    const startIndex = (currentPage.value - 1) * itemsPerPage
    return sortedStocks.value.slice(startIndex, startIndex + itemsPerPage)
})

const totalPages = computed(() => Math.ceil(sortedStocks.value.length / itemsPerPage))

const goToPage = (page) => {
    if (page >= 1 && page <= totalPages.value) {
        currentPage.value = page
    }
}
</script>

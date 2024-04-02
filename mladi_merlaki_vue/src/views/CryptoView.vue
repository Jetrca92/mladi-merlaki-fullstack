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
                                    <input class="input" style="width: 50%;" type="text" placeholder="Cryptocurrency name" id="search" name="name" v-model="filterInput" />
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
            <table class="table is-fullwidth is-hoverable" id="crypto-table" v-if="crypto.length > 0">
                <thead>
                    <tr>
                        <th class="is-info">#</th>
                        <th class="is-info">Stock</th>
                        <th class="is-info">Price</th>
                        <th class="is-info">Volume</th>
                        <th class="is-info">Market Cap</th>
                    </tr>
                </thead>
                <tbody>
                    <tr v-for="(coin, index) in pagedCrypto" :key="coin.id">
                        <th scope="row">{{ (currentPage - 1) * itemsPerPage + index + 1 }}</th>
                        <td><router-link :to="`/cryptocurrency/${coin.id}`" class="navbar-item"><img :src="coin.logo" style="width: 20px; height: auto; margin-right: 5px;" class="mr-3" alt="{{ coin.symbol }}">{{ coin.name }} ({{ coin.symbol }})</router-link></td>
                        <td>${{ coin.price}}</td>
                        <td>${{ coin.volume}}</td>
                        <td>${{ coin.market_cap}}</td>
                    </tr>
                </tbody>
            </table>
            <div v-else>
                No coins found.
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

const crypto = ref([])
const selectedSort = ref('-market_cap')
const filterInput = ref('')
const itemsPerPage = 100
let currentPage = ref(1)

// Get stock data from API
const getCryptoData = () => {
    axios.get(`api/v1/marketdata/crypto/`)
        .then(response => {
        crypto.value = response.data
        })
        .catch(error => {
        console.error(error)
        })
}
onMounted(getCryptoData)

// Filter and sort stocks
const sortedCrypto = computed(() => {
    const copiedCrypto = [...crypto.value]
    copiedCrypto.sort((a, b) => {
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
        return copiedCrypto.filter(coin => coin.name.toLowerCase().includes(filterInput.value.toLowerCase()));
    } 
    return copiedCrypto
})

// Pagination
const pagedCrypto = computed(() => {
    const startIndex = (currentPage.value - 1) * itemsPerPage
    return sortedCrypto.value.slice(startIndex, startIndex + itemsPerPage)
})

const totalPages = computed(() => Math.ceil(sortedCrypto.value.length / itemsPerPage))

const goToPage = (page) => {
    if (page >= 1 && page <= totalPages.value) {
        currentPage.value = page
    }
}
</script>

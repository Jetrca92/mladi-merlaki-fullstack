<template>
    <section class="section">
        <div class="page-sign-up">
            <div class="columns">
                <div class="column is-4 is-offset-4">
                    <h1 class="title">Log in</h1>
                    
                    <form @submit.prevent="submitForm">
                        <div class="field">
                            <label>Username</label>
                            <div class="control">
                                <input type="text" class="input" v-model="username">
                            </div>
                        </div>
                        <div class="field">
                            <label>Password</label>
                            <div class="control">
                                <input type="password" class="input" v-model="password">
                            </div>
                        </div>
                        <div class="notification is-danger" v-if="errors.length">
                            <p v-for="error in errors" v-bind:key="error">{{  error }}</p>
                        </div>
                        <div class="field">
                            <div class="control">
                                <button class="button is-info">Log in</button>
                            </div>
                        </div>
                        <hr>
                        Or <router-link to="/sign-up">click here</router-link> to sign up!
                    </form>

                </div>
            </div>
        </div>
    </section>
</template>

<script setup>
import axios from 'axios'
import { ref } from 'vue'
import { useRouter } from 'vue-router'

const username = ref('')
const password = ref('')
const errors = ref([])
const token = ref('')
const router = useRouter()

const submitForm = async () => {
    axios.defaults.headers.common["Authorization"] = ""

    const formData = {
        username: username.value,
        password: password.value
    }
    await axios.post("/api/v1/token/login/", formData)
        .then(response => {
            token.value = response.data.auth_token
            localStorage.setItem("token", token.value)
            // Mutate state using Vue 3's Composition API
            router.to('/')
        })
        
        .catch(error => {
            if (error.response) {
                for (const property in error.response.data) {
                    errors.value.push(`${property}: ${error.response.data[property]}`)
                }
            } else {
                errors.value.push('Something went wrong. Please try again.')
                console.log(JSON.stringify(error))
            }
        }) 
}
</script>
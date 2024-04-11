import { createStore } from 'vuex'
import axios from 'axios'


export default createStore({
  state: {
    isAuthenticated: false,
    token: '',
    portfolio: null
  },
  getters: {
  },
  mutations: {
    initializeStore(state) {
      if (localStorage.getItem('token')) {
        state.token = localStorage.getItem('token')
        state.isAuthenticated = true
      } else {
        state.token = ''
        state.isAuthenticated = false
      }
    },
    setToken(state, token) {
      state.token = token
      state.isAuthenticated = true
    },
    removeToken(state) {
      state.token = ''
      state.isAuthenticated = false
    },
    setPortfolio(state, portfolio) {
      state.portfolio = portfolio
    }
  },
  actions: {
    initializeStore({ commit} ) {
      commit('initializeStore')
    },
    async fetchPortfolio({ commit }) {
      try {
        const response = await axios.get(`api/v1/portfolio/portfolio/`)
        commit('setPortfolio', response.data)
      } catch (error) {
        console.error(error)
        // Handle error as needed
      }
    }
  },
  modules: {
  }
})

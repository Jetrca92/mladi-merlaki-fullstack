import { createStore } from 'vuex'
import axios from 'axios'

const HOUR_IN_MS = 3600000

export default createStore({
  state: {
    isAuthenticated: false,
    token: '',
    portfolio: null,
    appInfo: null,
    lastAppInfoFetchTime: null,
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
    },
    setAppInfo(state, appInfo) {
      state.appInfo = appInfo
    },
    setLastAppInfoFetchTime(state, time) {
      state.lastAppInfoFetchTime = time;
    },
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
      }
    },
    async fetchAppInfo({ commit, state }) {
      // Check if enough time has passed since the last API call
      if (!state.lastAppInfoFetchTime || Date.now() - state.lastAppInfoFetchTime >= HOUR_IN_MS) {
        try {
          const response = await axios.get('api/v1/marketdata/app_data/')
          commit('setAppInfo', response.data)
          commit('setLastAppInfoFetchTime', Date.now()); // Update last call timestamp
          return response.data;
        } catch (error) {
          console.error('Error fetching app info:', error)
          throw error;
        }
      } else {
        // If less than an hour has passed, return the cached data
        return state.appInfo;
      }
    },
  },
  modules: {
  }
})

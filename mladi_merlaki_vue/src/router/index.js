import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import SignupView from '../views/SignupView.vue'
import LoginView from '../views/LoginView.vue'
import UserPortfolio from '../views/UserPortfolio.vue'
import StocksView from '@/views/StocksView.vue'
import StockPageView from '@/views/StockPageView.vue'
import CryptoView from '@/views/CryptoView.vue'

const routes = [
  {
    path: '/',
    name: 'home',
    component: HomeView
  },
  {
    path: '/sign-up',
    name: 'signup',
    component: SignupView
  },
  {
    path: '/log-in',
    name: 'login',
    component: LoginView
  },
  {
    path: '/portfolio',
    name: 'portfolio',
    component: UserPortfolio
  },
  {
    path: '/stocks',
    name: 'stocks',
    component: StocksView
  },
  {
    path: '/cryptocurrency',
    name: 'cryptocurrency',
    component: CryptoView
  },
  {
    path: '/stocks/:id',
    name: 'stockpage',
    component: StockPageView
  }
]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
})

export default router

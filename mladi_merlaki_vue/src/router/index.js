import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import SignupView from '../views/SignupView.vue'
import LoginView from '../views/LoginView.vue'
import UserPortfolio from '../views/UserPortfolio.vue'
import StocksView from '@/views/StocksView.vue'
import StockPageView from '@/views/StockPageView.vue'
import CryptoView from '@/views/CryptoView.vue'
import CoinPageView from '@/views/CoinPageView.vue'
import LearnView from '@/views/LearnView.vue'
import HistoryView from '@/views/HistoryView.vue'
import RankingsView from '@/views/RankingsView.vue'

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
    path: '/stocks/:id',
    name: 'stockpage',
    component: StockPageView
  },
  {
    path: '/cryptocurrency',
    name: 'cryptocurrency',
    component: CryptoView
  },
  {
    path: '/cryptocurrency/:id',
    name: 'cryptopage',
    component: CoinPageView
  },
  {
    path: '/learn',
    name: 'learn',
    component: LearnView
  },
  {
    path: '/history',
    name: 'history',
    component: HistoryView
  },
  {
    path: '/rankings',
    name: 'rankings',
    component: RankingsView
  },
]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
})

export default router

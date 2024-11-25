import { createRouter, createWebHistory } from 'vue-router'

import market from '../views/market/index.vue'
const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'market',
      component: market
    },
    {
      path: '/home2',
      name: 'home2',
      component: () => import('../views/home.vue')
    },
    {
      path: '/information',
      name: 'information',
      component: () => import('../views/information.vue')
    },
    {
      path: '/chat',
      name: 'chat',
      component: () => import('../views/chat.vue')
    },
    {
      path: '/login',
      name: 'login',
      component: () => import('../views/login/login.vue')
    },
  ]
})

export default router

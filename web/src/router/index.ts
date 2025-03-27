import { createRouter, createWebHistory } from 'vue-router'

import ClientLayout from '../views/client/index.vue'
import AdminLayout from '../views/admin/index.vue'
import LoginLayout from '../views/login/index.vue'

import HomeView from '../views/client/home.vue'
const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      component: ClientLayout,
      children: [
        {
          path: '/',
          name: 'home',
          component: HomeView
        },
        {
          path: '/market',
          name: 'market',
          component: () => import('../views/client/market.vue')
        },
        {
          path: '/information',
          name: 'information',
          component: () => import('../views/client/information.vue')
        },
        {
          path: '/buy',
          name: 'buy',
          component: () => import('../views/client/buy.vue')
        },
        {
          path: '/sell',
          name: 'sell',
          component: () => import('../views/client/sell.vue')
        },
        {
          path: '/chat',
          name: 'chat',
          component: () => import('../views/client/chat.vue')
        },
      ]
    },
    {
      path: '/admin',
      component: AdminLayout,
      children: [
        {
          path: '/admin/information',
          name: 'admin-information',
          component: () => import('../views/admin/information.vue')
        },
        {
          path: '/admin/user',
          name: 'admin-user',
          component: () => import('../views/admin/user.vue')
        },
        {
          path: '/admin/commodity',
          name: 'admin-commodity',
          component: () => import('../views/admin/commodity.vue')
        },
      ]
    },
    {
      path: '/auth',
      component: LoginLayout,
      children: [
        {
          path: '/login',
          name: 'login',
          component: () => import('../views/login/login.vue')
        },
        {
          path: '/register',
          name: 'register',
          component: () => import('../views/login/register.vue')
        }
      ]
    },
  ]
})

export default router

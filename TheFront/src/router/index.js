/**
 * Arquivo: TheFront/src/router/index.js
 * Descrição:
 *   - Define as rotas do Vue Router, incluindo as páginas de login, dashboard e etc.
 */

import { createRouter, createWebHistory } from 'vue-router'
import Login from '@/components/Login.vue'
import SecureHome from '@/components/SecureHome.vue'
import AdminPanel from '@/components/AdminPanel.vue'
import QuantumKeyGen from '@/components/QuantumKeyGen.vue'
import DarkDashboard from '@/components/DarkDashboard.vue'

function isAuthenticated() {
  return !!localStorage.getItem('jwt_token')
}

function isAdmin() {
  return localStorage.getItem('user_role') === 'admin'
}

const routes = [
  { path: '/', name: 'Login', component: Login },
  {
    path: '/dashboard',
    name: 'DarkDashboard',
    component: DarkDashboard,
    beforeEnter: (to, from, next) => {
      if (!isAuthenticated()) return next('/')
      next()
    }
  },
  {
    path: '/secure',
    name: 'SecureHome',
    component: SecureHome,
    beforeEnter: (to, from, next) => {
      if (!isAuthenticated()) return next('/')
      next()
    }
  },
  {
    path: '/admin',
    name: 'AdminPanel',
    component: AdminPanel,
    beforeEnter: (to, from, next) => {
      if (!isAuthenticated()) return next('/')
      if (!isAdmin()) return next('/secure')
      next()
    }
  },
  {
    path: '/quantum',
    name: 'QuantumKeyGen',
    component: QuantumKeyGen,
    beforeEnter: (to, from, next) => {
      if (!isAuthenticated()) return next('/')
      next()
    }
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router

/*
MELHORIAS FUTURAS:
1. Usar decode do JWT (jwt-decode) para extrair role e user info, ao invés de localStorage estática.
2. Criar rota para 'Vault' e outra para 'Logs (Kerberos)', caso queira um painel unificado.
3. Adicionar animações de transição entre rotas (Vue transitions).
4. Tratar 404 - rotas inexistentes com uma tela customizada.
*/

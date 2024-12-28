/**
 * Arquivo: TheFront/src/router/index.js
 * Descrição:
 *   - Define as rotas do Vue Router, incluindo as páginas de login, dashboard e etc.
 */

import { createRouter, createWebHistory } from 'vue-router'

// Aqui estão os imports usando caminhos RELATIVOS
import Login from '../components/Login.vue'
import SecureHome from '../components/SecureHome.vue'
import AdminPanel from '../components/AdminPanel.vue'
import QuantumKeyGen from '../components/QuantumKeyGen.vue'
import DarkDashboard from '../components/Dashboard.vue'

function isAuthenticated() {
  // Checa se existe token no localStorage
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
1. Caso queira usar '@/components/...' em vez de '../components/...',
   configure o alias no vite.config.js e garanta que as pastas estejam corretas.
2. Decodificar o token JWT (com 'jwt-decode') para ler role de forma dinâmica, em vez de localStorage.
3. Adicionar rota de 404 caso o usuário tente acessar algo inexistente.
4. Criar rota de logout separada, se desejar redirecionamento e limpeza de dados.
*/

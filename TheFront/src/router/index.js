/*
Arquivo: TheFront/src/router/index.js
Descrição: Definição das rotas do Vue.js, incluindo a rota de login e uma rota protegida.
*/

import { createRouter, createWebHistory } from 'vue-router'
import Login from '../components/Login.vue'
import QuantumKeyGen from '../components/QuantumKeyGen.vue' // Exemplo de rota protegida

function isAuthenticated() {
  // Checa se existe token no localStorage
  const token = localStorage.getItem('jwt_token')
  return !!token
}

const routes = [
  { path: '/', name: 'Home', component: Login },
  {
    path: '/secure-page',
    name: 'SecurePage',
    component: QuantumKeyGen,
    beforeEnter: (to, from, next) => {
      if (!isAuthenticated()) {
        return next('/')
      }
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
1. Implementar guards mais robustos, verificando se o token ainda é válido (decodificar e checar exp).
2. Redirecionar para páginas diferentes dependendo do perfil de usuário (admin, user, etc.).
3. Integrar logs de navegação ou telemetria para análise de uso.
4. Criar rota /logout para invalidar o token e limpar dados locais.
*/

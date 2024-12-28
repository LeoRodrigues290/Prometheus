/**
 * Arquivo: TheFront/src/main.js
 * Descrição:
 *   - Ponto de entrada da aplicação Vue.js, carregando Tailwind (index.css) e roteador.
 */

import { createApp } from 'vue'
import App from './App.vue'
import router from './router/index.js'

// Importante: carrega o Tailwind e estilos globais
import './index.css'

const app = createApp(App)
app.use(router)
app.mount('#app')

/*
MELHORIAS FUTURAS:
1. Adicionar um store (Pinia/Vuex) para gerenciar estado (token, dados do usuário).
2. Configurar interceptors do axios para inserir token JWT nas requisições.
3. Integrar monitoramento de erros e logs.
*/

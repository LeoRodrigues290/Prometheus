/**
 * Arquivo: TheFront/src/main.js
 * Descrição: Ponto de entrada do front-end em Vue.js.
 */

import { createApp } from 'vue'
import App from './App.vue'
import router from './router'

const app = createApp(App)
app.use(router)
app.mount('#app')

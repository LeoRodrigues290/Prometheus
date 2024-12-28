/**
 * Arquivo: TheFront/vite.config.js
 * Descrição:
 *   - Configuração do Vite para build e dev server.
 */

import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

export default defineConfig({
  plugins: [vue()],
  server: {
    port: 5173
    // Se precisar de proxy para evitar CORS:
    // proxy: {
    //   '/api': 'http://localhost:8000'
    // }
  },
  build: {
    outDir: 'dist',
    sourcemap: true
  }
})

/*
MELHORIAS FUTURAS:
1. Configurar proxy se quiser chamar endpoints (/login, /pyramid, etc.) sem lidar com CORS.
2. Adicionar plugins de análise de bundle (rollup-plugin-visualizer) para otimizar o build.
3. Integrar variáveis de ambiente para separar dev/staging/production.
*/

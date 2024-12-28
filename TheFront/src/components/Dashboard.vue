<template>
  <div class="min-h-screen bg-dark-bg text-gray-100">
    <!-- Barra lateral -->
    <aside class="hidden md:block w-64 bg-dark-surface h-full fixed top-0 left-0 pt-16">
      <nav class="flex flex-col space-y-4 px-4">
        <div class="py-2 px-3 rounded hover:bg-dark-highlight transition-colors cursor-pointer" @click="goTo('/dashboard')">
          Dashboard
        </div>
        <div class="py-2 px-3 rounded hover:bg-dark-highlight transition-colors cursor-pointer" @click="goTo('/quantum')">
          Geração de Chaves
        </div>
        <div class="py-2 px-3 rounded hover:bg-dark-highlight transition-colors cursor-pointer" @click="goTo('/secure')">
          Área Segura
        </div>
        <div class="py-2 px-3 rounded hover:bg-dark-highlight transition-colors cursor-pointer" v-if="userRole === 'admin'" @click="goTo('/admin')">
          Admin Panel
        </div>
        <div class="py-2 px-3 rounded hover:bg-red-600 transition-colors cursor-pointer mt-8" @click="logout">
          Sair
        </div>
      </nav>
    </aside>

    <!-- Conteúdo Principal -->
    <div class="md:ml-64 p-6 pt-16">
      <h1 class="text-2xl font-bold mb-4">Painel Prometheus</h1>
      <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
        <!-- Card de exemplo -->
        <div class="bg-dark-surface rounded p-4">
          <h2 class="text-lg font-semibold mb-2">Atividade Semanal</h2>
          <p class="text-sm">Exemplo de dados, ex.: 120 chaves geradas</p>
        </div>
        <!-- Card de exemplo -->
        <div class="bg-dark-surface rounded p-4">
          <h2 class="text-lg font-semibold mb-2">Eventos Recentes</h2>
          <ul class="text-sm list-disc list-inside">
            <li>Chave gerada em 29/09</li>
            <li>Login admin em 29/09</li>
            <li>Vault access em 28/09</li>
          </ul>
        </div>
        <!-- Card de exemplo -->
        <div class="bg-dark-surface rounded p-4">
          <h2 class="text-lg font-semibold mb-2">Sistema</h2>
          <p class="text-sm">Status: Online</p>
          <p class="text-sm">Versão: 1.0.0</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'Dashboard',
  data() {
    return {
      userRole: localStorage.getItem('user_role') || 'user'
    }
  },
  methods: {
    goTo(path) {
      this.$router.push(path)
    },
    logout() {
      localStorage.removeItem('jwt_token')
      localStorage.removeItem('user_role')
      this.$router.push('/')
    }
  }
}
</script>

<style scoped>
/* Se precisar de estilos adicionais */
</style>

<!--
MELHORIAS FUTURAS:
1. Substituir os itens de demonstração por dados reais (ex.: logs via Kerberos, chaves geradas via Pyramid).
2. Integrar gráficos usando Chart.js ou ECharts, com paleta dark.
3. Tornar a sidebar responsiva com animação (ex.: abrir/fechar em telas menores).
4. Adicionar widgets extras (estatísticas de uso, alertas de segurança, etc.).
-->

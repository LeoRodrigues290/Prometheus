<template>
  <div id="app" class="min-h-screen flex flex-col">
    <!-- Barra Superior -->
    <header class="bg-dark-surface text-white py-4 px-6 flex items-center">
      <img src="@/assets/logo.svg" alt="Logo" class="h-8 mr-4" />
      <h1 class="text-xl font-bold uppercase">Prometheus Security</h1>
    </header>

    <!-- Conteúdo dinamicamente injetado -->
    <main class="flex-1">
      <router-view />
    </main>
  </div>
</template>

<script>
export default {
  name: 'App'
}
</script>

<style scoped>
/* Exemplo: personalizar scrollbars, etc. */
::-webkit-scrollbar {
  width: 8px;
}
::-webkit-scrollbar-thumb {
  background-color: #333;
}
::-webkit-scrollbar-track {
  background-color: #1A1A1A;
}
</style>

<!--
MELHORIAS FUTURAS:
1. Incluir menu lateral fixo (side nav) com ícones, remetendo a interface moderna.
2. Adicionar um rodapé ou status bar com informações do sistema.
3. Criar tema adicional “antigo” com texturas ou efeitos de “desgaste” (usando imagens leves).
-->

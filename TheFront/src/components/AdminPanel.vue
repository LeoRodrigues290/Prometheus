<template>
  <div class="flex flex-col items-center justify-center min-h-screen bg-dark-bg text-white">
    <h2 class="text-3xl font-bold mb-4">Painel Administrativo</h2>
    <p class="mb-6">Apenas usuários com privilégios de administração podem ver esta página.</p>
    <button @click="handleLogout" class="bg-dark-highlight px-4 py-2 rounded hover:bg-dark-accent transition-colors">
      Sair
    </button>
  </div>
</template>

<script>
export default {
  name: 'AdminPanel',
  methods: {
    handleLogout() {
      localStorage.removeItem('jwt_token')
      localStorage.removeItem('user_role')
      this.$router.push('/')
    }
  }
}
</script>

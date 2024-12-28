<template>
  <div class="flex flex-col items-center justify-center min-h-screen bg-dark-bg text-white">
    <h2 class="text-3xl font-bold mb-4">Área Segura</h2>
    <p class="mb-6">Bem-vindo(a)! Você está autenticado.</p>
    <button @click="handleLogout" class="bg-red-600 px-4 py-2 rounded hover:bg-red-700 transition-colors">
      Sair
    </button>
  </div>
</template>

<script>
export default {
  name: 'SecureHome',
  methods: {
    handleLogout() {
      localStorage.removeItem('jwt_token')
      localStorage.removeItem('user_role')
      this.$router.push('/')
    }
  }
}
</script>

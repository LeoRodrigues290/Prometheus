<template>
  <div class="flex items-center justify-center min-h-screen bg-dark-bg">
    <div class="bg-dark-surface p-8 rounded shadow-md w-80">
      <h2 class="text-2xl mb-4 font-semibold">Acesso ao Prometheus</h2>
      <form @submit.prevent="handleLogin">
        <div class="mb-4">
          <label class="block mb-1 font-medium">Usuário</label>
          <input
            v-model="username"
            type="text"
            class="w-full p-2 bg-dark-panel focus:outline-none focus:ring-2 focus:ring-dark-highlight rounded"
            required
          />
        </div>
        <div class="mb-4">
          <label class="block mb-1 font-medium">Senha</label>
          <input
            v-model="password"
            type="password"
            class="w-full p-2 bg-dark-panel focus:outline-none focus:ring-2 focus:ring-dark-highlight rounded"
            required
          />
        </div>
        <button
          type="submit"
          class="w-full bg-dark-highlight py-2 rounded mt-2 hover:bg-dark-accent transition-colors"
        >
          Entrar
        </button>
      </form>
      <p v-if="errorMessage" class="text-red-500 mt-4">{{ errorMessage }}</p>
    </div>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  name: 'Login',
  data() {
    return {
      username: '',
      password: '',
      errorMessage: ''
    }
  },
  methods: {
    async handleLogin() {
      try {
        // Limpa qualquer mensagem de erro anterior
        this.errorMessage = ''

        const formData = new URLSearchParams()
        formData.append('username', this.username)
        formData.append('password', this.password)

        const response = await axios.post('http://127.0.0.1:8000/login', formData, {
          headers: { 'Content-Type': 'application/x-www-form-urlencoded' }
        })

        const { access_token } = response.data
        localStorage.setItem('jwt_token', access_token)

        // Exemplo simples de role
        if (this.username === 'admin') {
          localStorage.setItem('user_role', 'admin')
        } else {
          localStorage.setItem('user_role', 'user')
        }

        this.$router.push('/dashboard')
      } catch (err) {
        if (err.response && err.response.data && err.response.data.message) {
          // Mensagem específica do backend
          this.errorMessage = err.response.data.message
        } else if (err.request) {
          // Requisição foi feita, mas nenhuma resposta foi recebida
          this.errorMessage = 'Falha no login: serviço indisponível.'
        } else {
          // Algo aconteceu na configuração da requisição que acionou um erro
          this.errorMessage = 'Falha no login: erro inesperado.'
        }

        // Opcional: Logar o erro no console para depuração
        console.error('Erro no login:', err)
      }
    }
  }
}
</script>

<style scoped>
/* Adicione estilos personalizados aqui, se necessário */
</style>

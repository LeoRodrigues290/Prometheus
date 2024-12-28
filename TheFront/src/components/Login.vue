<!--
Arquivo: TheFront/src/components/Login.vue
Descrição:
    - Componente Vue para login de usuário.
    - Faz requisição ao endpoint /login do back-end e obtém o token JWT.
-->

<template>
  <div class="login-container">
    <h1>Login</h1>
    <form @submit.prevent="handleLogin">
      <div class="input-group">
        <label>Usuário</label>
        <input v-model="username" type="text" />
      </div>
      <div class="input-group">
        <label>Senha</label>
        <input v-model="password" type="password" />
      </div>
      <button type="submit">Entrar</button>
    </form>
    <p v-if="errorMessage" class="error">{{ errorMessage }}</p>
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
        const response = await axios.post('http://localhost:8000/login', {
          username: this.username,
          password: this.password
        }, {
          // Formato para OAuth2PasswordRequestForm
          headers: {
            'Content-Type': 'application/x-www-form-urlencoded'
          },
          params: {
            // O FastAPI OAuth2PasswordRequestForm espera 'username' e 'password'
            'username': this.username,
            'password': this.password
          }
        })
        const { access_token } = response.data
        localStorage.setItem('jwt_token', access_token)
        this.$router.push('/secure-page')
      } catch (error) {
        this.errorMessage = 'Falha no login. Verifique usuário e senha.'
      }
    }
  }
}
</script>

<style scoped>
.login-container {
  background-color: #222;
  color: #fff;
  padding: 20px;
  border-radius: 4px;
}
.input-group {
  margin-bottom: 10px;
}
.error {
  color: #ff6666;
  margin-top: 10px;
}
</style>

<!--
MELHORIAS FUTURAS:
1. Substituir localStorage por cookies seguros (HttpOnly) para evitar vulnerabilidades de XSS.
2. Adicionar validação mais detalhada de formulários (campos obrigatórios, regex, etc.).
3. Redirecionar automaticamente para /login caso o token JWT expire.
4. Exibir avisos personalizados (toasters, modals) em caso de erro.
-->

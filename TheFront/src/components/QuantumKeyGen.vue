<!-- Arquivo: TheFront/src/components/QuantumKeyGen.vue -->
<template>
  <div class="keygen-container">
    <h2>Gerar Chave Quântica</h2>
    <button @click="generateKey">Gerar</button>
    <p v-if="quantumKey">Chave Gerada: {{ quantumKey }}</p>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  name: 'QuantumKeyGen',
  data() {
    return {
      quantumKey: ''
    }
  },
  methods: {
    async generateKey() {
      try {
        const response = await axios.get('http://localhost:8000/pyramid/generate_key')
        this.quantumKey = response.data.quantum_key
      } catch (error) {
        console.error(error)
      }
    }
  }
}
</script>

<style scoped>
.keygen-container {
  background-color: #222;
  padding: 20px;
  color: #fff;
  border-radius: 4px;
}
button {
  background-color: #444;
  color: #fff;
  border: none;
  padding: 10px;
  cursor: pointer;
  border-radius: 4px;
}
button:hover {
  background-color: #666;
}
</style>

<!--
MELHORIAS FUTURAS:
1. Integrar sistema de autenticação para que apenas usuários logados possam gerar chaves.
2. Exibir mensagens de erro detalhadas para o usuário em caso de falha no endpoint.
3. Implementar WebSockets ou Server-Sent Events para notificar o front-end em tempo real sobre eventos do sistema.
4. Adicionar suporte multilíngue (i18n) para internacionalizar e localizar a aplicação.
-->
